function _solvesend(v) {
	console.warn(v)
	ws.send(JSON.stringify(v))
}

function launch(x, y){
	v = {
        type: "launch",
        value: {dx: x, dy: y}
    }
	_solvesend(v)
};



var gotoX = null;
var gotoY = null;

var solve = null;
var cursolveidx = 0;
var _lock = false;
var _lastval = null;

function _ismoving(val) {
	if(_lastval == null) {
		_lastval = val;
		return true
	}
	var res = true;
	if(_lastval.x === val.x && _lastval.y === val.y)
		res = false;
	_lastval = val;
	return res


}
function calcForce(target, cur) {
	var dir = (target - cur) / Math.abs(target - cur)
	var mag = Math.min(Math.abs(target - cur), 0.15)
	
    return dir * mag
}

function customListen(msg){
	let data;
	try {
		data = JSON.parse(msg.data);
	} catch(e) {}
    if(data.type === "collider") {
        console.log(data.value);
        return;
    }

    if(data.type !== "ball") {
        return;
    }
    if(_ismoving(data.value)){
		_lock = false
        console.log(data.value)
        return;
    }
    var val = data.value;
	if(solve !== null) {
		if(_lock)
			return;
		if(cursolveidx >= solve.length){
			solve = null;
			cursolveidx = 0;
			return
		}
		_solvesend(solve[cursolveidx]);
		cursolveidx++;
		_lock = true;
		
		return
	}
	// if(_lock)
	// 	return;
    if(gotoX !== null){
		console.log(val.x);
		if(val.x === gotoX){
			gotoX = null;
			return;
		}

		//console.log("forcex:", calcForce(gotoX, val.x))
		//_lock = true;
        launch(calcForce(gotoX, val.x), 0);
    }
    else if(gotoY !== null) {
		console.log(val.y);
		if(val.y === gotoY){
			gotoY = null;
			return;
		}
		//_lock= true;
		//console.log("forcey:", calcForce(gotoY, val.y))
        launch(0, calcForce(gotoY, val.y));
    }
    return;
}


document.addEventListener("mouseup", e => {
	mousedown = false;
	mouse.x2 = e.x;
	mouse.y2 = e.y;
	if (ws.readyState === ws.OPEN) {
		console.warn(JSON.stringify({
			type: "launch",
			value: {
				dx: (mouse.x1 - mouse.x2) / SLOWNESS,
				dy: (mouse.y1 - mouse.y2) / SLOWNESS
			}
		}));
	}
});

solve0 = [
	{"type":"launch","value":{"dx":8.25,"dy":4.7}},
	{"type":"launch","value":{"dx":7.15,"dy":-3.2}},
	{"type":"launch","value":{"dx":17.05,"dy":2.1}},
	{"type":"launch","value":{"dx":-9.3,"dy":0.6}}
	//{"type":"launch","value":{"dx":-4.05,"dy":0.8}}
]

solve1 = [
	{"type":"launch","value":{"dx":17,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":9.6}},
	{"type":"launch","value":{"dx":-17,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":-8.5}},
	{"type":"launch","value":{"dx":15.5,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":7.6}},
	{"type":"launch","value":{"dx":15,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":-6.6}},
	{"type":"launch","value":{"dx":13.3,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":5}},
	{"type":"launch","value":{"dx":-12,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":-4}},
	{"type":"launch","value":{"dx":11,"dy":0}},
	{"type":"launch","value":{"dx":0,"dy":2.9125}},
	{"type":"launch","value":{"dx":-10, "dy":0}},
	{"type":"launch","value":{"dx":0,"dy":-1.4}},
]



ws.addEventListener("message", customListen)

function draw() {
	//console.log(ball);
	if (ball) {
		c.clearRect(0, 0, cnv.width, cnv.height);
		for (let col of colliders) {
			c.fillStyle = "gray";
			c.fillRect(...col);
			c.fill();
		}
		c.beginPath();
		c.fillStyle = "#DD2F2F";
		c.arc(flag.x, flag.y, flag.r, 0, 2 * Math.PI);
		c.fill();
		c.beginPath();
		c.fillStyle = `rgba(110,110,200,1)`;
		c.arc(ball.x, ball.y, ball.r, 0, 2 * Math.PI);
		c.fill();
		if (mousedown && !ball.moving) {
			c.beginPath();
			c.fillStyle = "#BDBDBD";
			c.arc(ball.x, ball.y, 3, 0, 2 * Math.PI);
			c.arc(ball.x + (mouse.x2 - mouse.x1), ball.y + (mouse.y2 - mouse.y1), 3, 0, 2 * Math.PI);
			c.fill();
			c.beginPath();
			c.lineWidth = 6;
			c.strokeStyle = "#BDBDBD";
			c.moveTo(ball.x, ball.y);
			c.lineTo(ball.x + (mouse.x2 - mouse.x1), ball.y + (mouse.y2 - mouse.y1));
			c.stroke();
		}
	}
	requestAnimationFrame(draw);
}


solve=solve0