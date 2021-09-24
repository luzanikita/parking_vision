let aoiCollection = {};
let newAoi;
let selectedAoi;
let video;
let statusData;
let predictionData;
let img_path;
let cueId;
let canvas;

let frame_i = 0;
let fr = 30;
let cameraId = 2;
let minTestCounts = 3;

async function setup() {
	aoiCollection = {};
	pixelDensity(1);
	video = select("#video");
	if (canvas != undefined) {
		videoStream.removeCue(cueId);
		canvas.remove();
	}
	videoStream = createVideo([`/static/camera_${cameraId}.mp4`]);
	videoStream.hide();
	videoStream.loop();
	cueId = videoStream.addCue(0.01, refreshFrameCount);
	canvas = createCanvas(0, 0);
	fitCanvasToVideo();
	frameRate(30);
	let deleteButton = select("#delete");
	deleteButton.mousePressed(deleteAoi);

	await initAoiList();
}

function refreshFrameCount() {
	frame_i = 0;
}

function windowResized() {
	fitCanvasToVideo();
}

function fitCanvasToVideo() {
	videoSize = video.size();
	videoPosition = video.position();
	canvas.position(videoPosition.x, videoPosition.y);
	resizeCanvas(videoSize.width, videoSize.height);
}

async function draw() {
	clear();
	image(videoStream, 0, 0, videoSize.width, videoSize.height);
	if (frame_i % (2*fr) == 0) {
		img_path = `camera_${cameraId}_${frame_i}.png`
		// save(img_path);
		updateCall(img_path);
	}

	for (let id in aoiCollection) {
		aoiCollection[id].show();
	}

	if (newAoi != undefined && newAoi.isResizing) {
		newAoi.resize(mouseX, mouseY);
		newAoi.show();
	}

	frame_i++;
}

async function mouseClicked() {
	if (!isOnCanvas(mouseX, mouseY)) {
		return;
	}
	if (newAoi != undefined && newAoi.isResizing) {
		await addAoi();
	} else {
		selectedAoi = getSelectedAoi();
	}
	if (selectedAoi != undefined) {
		console.log(selectedAoi);
	}
}

async function addAoi() {
	newAoi.stopResizing();
	if (newAoi.xSide > 10) {
		selectedAoi = newAoi;
		await postLot(newAoi, cameraId=cameraId);
	} else {
		console.log("Too small AoI.")
	}
}

function doubleClicked() {
	if (isOnCanvas(mouseX, mouseY))
		createAoi(mouseX, mouseY);
}

function isOnCanvas(x, y) {
	return (
		x < width &&
		x > 0 &&
		y < height &&
		y > 0
	)
}

function createAoi(x, y) {
	deselectAll();
	newAoi = new AOI(x, y);
	newAoi.isSelected = true;
}

function deselectAll() {
	for (let id in aoiCollection) {
		aoiCollection[id].isSelected = false;
	}
}

function getSelectedAoi() {
	deselectAll();
	let minDist = Number.MAX_VALUE;
	let minIndex;
	let aoi;
	for (let id in aoiCollection) {
		aoi = aoiCollection[id];
		if (aoi.isClicked(mouseX, mouseY)) {
			let aoiDist = aoi.distance(mouseX, mouseY);
			if (aoiDist < minDist) {
				minDist = aoiDist;
				minIndex = id;
			}
		}
	}
	aoi = aoiCollection[minIndex];
	if (aoi != undefined) {
		aoi.isSelected = true;
		aoi.index = minIndex;
	}
	return aoi;
}

async function deleteAoi() {
	if (selectedAoi != undefined) {
		console.log(selectedAoi);
		delete aoiCollection[selectedAoi.id];
		await deleteLot(selectedAoi.id);
		selectedAoi = undefined;
	}
}

class AOI {
	constructor(x, y, side=1, id=undefined, isFree=undefined) {
		this.x = x;
		this.y = y;
		this.xSide = side;
		this.ySide = side;
		this.id = id;
		this.isFree=isFree;
		this.isResizing = true;
		this.isSelected = false;
		this.index;
		this.predictions = [];
	}

	resize(x, y) {
		let w = max(0, min(x, width)) - this.x;
		let h = max(0, min(y, height)) - this.y;
		let xSide = w;
		let ySide = h;

		if (abs(w) < abs(h))
			xSide = abs(h) * Math.sign(w);
		else
			ySide = abs(w) * Math.sign(h);

		if (this.x + xSide > width) {
			xSide = width - this.x;
			ySide = xSide * Math.sign(ySide);
		}
		else if (this.y + ySide > height) {
			ySide = height - this.y;
			xSide = ySide * Math.sign(xSide);
		}
		else if (this.x + xSide < 0) {
			xSide = -this.x;
			ySide = this.x * Math.sign(ySide);
		}
		else if (this.y + ySide < 0) {
			ySide = -this.y;
			xSide = this.y * Math.sign(xSide);
		}

		this.xSide = xSide;
		this.ySide = ySide;
	}

	stopResizing() {
		this.isResizing = false;
		let x = this.x + this.xSide;
		let y = this.y + this.ySide;
		if (this.xSide < 0) {
			this.x = x;
			this.xSide = abs(this.xSide);
		}
		if (this.ySide < 0) {
			this.y = y;
			this.ySide = abs(this.ySide);
		}
	}

	show() {
		let aoiColor;
		if (this.isFree == undefined)
			aoiColor = color(255, 255, 255);
		else if (this.isFree)
			aoiColor = color(0, 255, 0);
		else
			aoiColor = color(255, 0, 0);
	
		strokeWeight(2);
		stroke(aoiColor);

		aoiColor.setAlpha(64);
		if (this.isSelected)
			fill(aoiColor);
		else
			noFill();

		rect(this.x, this.y, this.xSide, this.ySide);
	}

	isClicked(x, y) {
		return (
			x > this.x && 
			x < this.x + this.xSide && 
			y > this.y && 
			y < this.y + this.ySide
		);
	}

	distance(x, y) {
		return dist(
			this.x + this.xSide / 2, 
			this.y + this.ySide / 2, 
			x, 
			y
		);
	}
}

async function postLot(aoi, cameraId) {
	const url = 'http://127.0.0.1:5000/api/lots';
	let body = {
		"camera_id": cameraId,
		"x": aoi.x,
		"y": aoi.y,
		"side": aoi.xSide
	}
	await fetch(url, {  
		method: 'post',  
		headers: {  
			"Content-type": "application/json"  
		},  
		body: JSON.stringify(body)
	})
	.then(  
		function(response) {  
			if (response.status !== 201) {  
				console.log('Error. Status Code: ' + response.status);  
				return;
			}
			response.json().then(function(data) {
				newAoi.id = data.id;
				aoiCollection[newAoi.id] = newAoi;
			});
		}  
	  )  
	  .catch(function(err) {  
		console.log('Fetch Error :-S', err);  
	  });
}

async function deleteLot(lot_id) {
	const url = `http://127.0.0.1:5000/api/lots/${lot_id}`;
	fetch(url, {  
		method: 'delete',  
		headers: {  
			"Content-type": "application/json"  
		},  
	})
	.then(  
		function(response) {  
			if (response.status !== 204) {  
				console.log('Error. Status Code: ' + response.status);  
				return;
			} else {
				console.log(`Lot ${lot_id} has been deleted.`);
				return;
			}
			// response.json().then(function(data) {
			// });
		}  
	  )  
	  .catch(function(err) {  
		console.log('Fetch Error :-S', err);  
	  });
}

async function getStatus(cameraId) {
	const url = `http://127.0.0.1:5000/api/cameras/${cameraId}/status`;
	await fetch(url)  
	.then(  
	  function(response) {  
		if (response.status !== 200) {  
			console.log('Error. Status Code: ' + response.status);  
		  	return;
		}
		response.json().then(function(data) {
			statusData = data;
		});
	  }  
	)  
	.catch(function(err) {  
	  console.log('Fetch Error :-S', err);  
	});
}

async function getPredictions(data, img_path) {
	data.img_path = img_path;
	console.log(cameraId, frame_i, img_path);
	const url = 'http://127.0.0.1:5001/predict';
	await fetch(url, {  
		method: 'post',  
		headers: {  
			"Content-type": "application/json"  
		},  
		body: JSON.stringify(data)
	})
	.then(  
		function(response) {  
			if (response.status !== 200) {
				console.log('Error. Status Code: ' + response.status);  
				return;
			}
			response.json().then(function(data) {
				predictionData = data;
				console.log(data);
			});
		}  
	  )  
	  .catch(function(err) {
		console.log(aoiCollection);
		console.log(data);
		console.log('Fetch Error :-S', err);  
		console.log(img_path);
	  });
}

async function updateStatus(status) {
	const url = 'http://127.0.0.1:5000/api/status';
	await fetch(url, {  
		method: 'post',  
		headers: {  
			"Content-type": "application/json"  
		},  
		body: JSON.stringify(status)
	})
	.then(  
		function(response) {  
			if (response.status !== 201) {  
				console.log('Error. Status Code: ' + response.status);  
				return;
			}
			response.json().then(function(data) {
				console.log(data);
			});
		}  
	  )  
	  .catch(function(err) {  
		console.log('Fetch Error :-S', err);  
	  });
}


async function initAoiList() {
	await getStatus(cameraId);
	aoiCollection = {}
	if (statusData != undefined) {
		statusData.lots.forEach(
			lot => {
				aoiCollection[lot.id] = new AOI(lot.x, lot.y, lot.side, lot.id, lot.is_free);
			}
		);
	}
}

async function updateCall(img_path) {
	await getStatus(cameraId=cameraId);
	if (statusData != undefined && statusData.lots.length > 0) {;
		await getPredictions(statusData, img_path);
		if (predictionData != undefined) {
			for (let i = 0; i < predictionData.statuses.length; i++) {
				let statusNew = predictionData.statuses[i];
				let statusOld = aoiCollection[statusNew.lot_id]
				if (statusOld == undefined)
					return;
				aoiCollection[statusNew.lot_id].predictions.push(statusNew.is_free);
				if (
					aoiCollection[statusNew.lot_id].predictions.length > 1 && 
					aoiCollection[statusNew.lot_id].predictions[0] != statusNew.is_free
				)
					aoiCollection[statusNew.lot_id].predictions = [statusNew.is_free];
				if (aoiCollection[statusNew.lot_id].predictions.length == minTestCounts) {
					let aggregatedPrediction = aoiCollection[statusNew.lot_id]
						.predictions
						.reduce((a, b) => a + b, 0);
					aoiCollection[statusNew.lot_id].predictions = [];
					if (aggregatedPrediction == 0 || aggregatedPrediction == minTestCounts) {
						aggregatedPrediction = aggregatedPrediction == minTestCounts;
						if (statusOld != undefined && aggregatedPrediction != statusOld.isFree) {
							aoiCollection[statusNew.lot_id].isFree = aggregatedPrediction;
							updateStatus(statusNew);
						}
					}
				}
			}
			predictionData = undefined;
		}
	}
}
