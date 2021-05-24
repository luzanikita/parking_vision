let aoiList = [];
let newAoi;
let selectedAoi;
let video;
let i = 0;

function setup() {
	pixelDensity(1);
	video = select("#video");
	// video.src = "../data/parking_3.mp4";
	videoStream = createVideo(["../data/parking_3.mp4"]);
	videoStream.hide();
	videoStream.loop();
	canvas = createCanvas(0, 0);
	fitCanvasToVideo();
	let deleteButton = select("#delete");
	deleteButton.mousePressed(deleteAoi);
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

function draw() {
	clear();
	videoPosition = video.position();
	image(videoStream, videoPosition.x, videoPosition.y);
	// i++;
	// if (i == 100) {
	// 	save('myCanvas.png');
	// 	i = 0;
	// }
	let aoi;
	for (let i = 0; i < aoiList.length; i++) {
		aoi = aoiList[i];
		aoi.classify();
		aoi.show();
	}
	
	if (newAoi != undefined && newAoi.isResizing) {
		newAoi.resize(mouseX, mouseY);
		newAoi.show();
	}
}

function mouseClicked() {
	if (!isOnCanvas(mouseX, mouseY))
		return;

	if (newAoi != undefined && newAoi.isResizing) {
		newAoi.stopResizing();
		newAoi.index = aoiList.length;
		aoiList.push(newAoi);
		selectedAoi = newAoi;
	} else {
		selectedAoi = getSelectedAoi();
	}
	if (selectedAoi != undefined) {
		console.log(selectedAoi);
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
}

function deselectAll() {
	for (let i = 0; i < aoiList.length; i++) {
		aoi = aoiList[i];
		aoi.isSelected = false;
	}
}

function getSelectedAoi() {
	deselectAll();
	let minDist = Number.MAX_VALUE;
	let minIndex = -1;
	let aoi;
	for (let i = 0; i < aoiList.length; i++) {
		aoi = aoiList[i];
		if (aoi.isClicked(mouseX, mouseY)) {
			let aoiDist = aoi.distance(mouseX, mouseY);
			if (aoiDist < minDist) {
				minDist = aoiDist;
				minIndex = i;
			}
		}
	}
	aoi = aoiList[minIndex];
	if (aoi != undefined) {
		aoi.isSelected = true;
		aoi.index = minIndex;
	}
	return aoi;
}

function deleteAoi() {
	if (selectedAoi != undefined) {
		aoiList.splice(selectedAoi.index, 1);
		selectedAoi = undefined;
	}
}

function classify(aoi) {
	aoi.isFree = Math.random() > 0.1;
}

class AOI {
	constructor(x, y, side=1) {
		this.x = x;
		this.y = y;
		this.xSide = side;
		this.ySide = side;
		this.isResizing = true;
		this.isSelected = true;
		this.isFree;
		this.index;
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

	classify() {
		// TODO:
		this.isFree = Math.random() < 0.1;
	}
}
