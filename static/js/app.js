const canvas = document.getElementById("radar")
const ctx = canvas.getContext("2d")

canvas.width = 420
canvas.height = 420

let centerX = canvas.width/2
let centerY = canvas.height/2
let maxRadius = 180


let sweepAngle = 0;
let wifiNetworks = [];


/* ===============================
   HELPER FUNCTIONS
================================ */

function hashAngle(mac){

let hash = 0;

for (let i = 0; i < mac.length; i++){
hash += mac.charCodeAt(i);
}

return (hash % 360) * Math.PI / 180;

}

/* Onw graph drawing function */

function drawChannelGraph(channels){

let canvas=document.getElementById("channelGraph")
let ctx=canvas.getContext("2d")

canvas.width = canvas.clientWidth
canvas.height = canvas.clientHeight

ctx.clearRect(0,0,canvas.width,canvas.height)

let i=0

for(let ch in channels){

let count=channels[ch]
let height = count * 18

ctx.fillStyle="#00ffaa"

ctx.fillRect(i*50,canvas.height-height, 35, height)

ctx.fillStyle="#00ff88"
ctx.fillText(ch,i*50+10,canvas.height-5)

i++
}
}


function drawDensityTimeline(history){

let canvas=document.getElementById("densityChart")
let ctx=canvas.getContext("2d")

canvas.width = canvas.clientWidth
canvas.height = canvas.clientHeight

ctx.clearRect(0,0,canvas.width,canvas.height)

ctx.strokeStyle="#00ff88"
ctx.beginPath()

for(let i=0;i<history.length;i++){

let x=i*8
let y=canvas.height-history[i]/20
 
if(i===0) ctx.moveTo(x,y)
else ctx.lineTo(x,y)
}

ctx.stroke()
}


function rssiToDistance(rssi){

let normalized = Math.max(-90, Math.min(-30, rssi));
let distance = (normalized + 90) / 60;

return distance * maxRadius;

}


/* ===============================
   DATA UPDATE
================================ */

async function updateData(){

let res = await fetch("/scan");
let data = await res.json();

wifiNetworks = data.wifi || [];

/* =============================
   EXTRA PANELS
============================= */

let strongest = -999
let weakest = 0

for (let n of wifiNetworks){

if (n.rssi > strongest) strongest = n.rssi
if (n.rssi < weakest) weakest = n.rssi

}

if(data.presence){

let txt=""

for(let p of data.presence){
txt+=p.bssid+"  "+p.duration+"s\n"
}

document.getElementById("presence").innerText=txt
}
if(data.motion){

let txt=""

for(let m of data.motion){

let v=m.velocity

let label="stable"

if(v>2) label="approaching"
if(v<-2) label="leaving"

txt+=m.bssid+"  "+label+"  "+v+" dBm/s\n"
}

document.getElementById("motion").innerText=txt
}


let avg = wifiNetworks.reduce((a,b)=>a+b.rssi,0)/wifiNetworks.length

document.getElementById("rf-metrics").innerText =
"Strongest signal: " + strongest + " dBm\n" +
"Weakest signal: " + weakest + " dBm\n" +
"Average signal: " + avg.toFixed(1) + " dBm\n" +
"Networks detected: " + wifiNetworks.length

if (data.rf_activity){

let a = data.rf_activity;

document.getElementById("rf-activity").innerText =
"Total networks: " + a.total_networks + "\n" +
"Hidden networks: " + a.hidden_networks + "\n" +
"Hotspots: " + a.hotspots;

}


/* SIGNAL HISTOGRAM */

if (data.histogram){

let txt = "";

for (let b in data.histogram){

txt += b + " dBm " + "█".repeat(data.histogram[b]) + "\n";

}

document.getElementById("signal-histogram").innerText = txt;

}


/* VENDOR BREAKDOWN */

if (data.vendors){

let vtxt = "";

for (let v in data.vendors){

vtxt += v + ": " + data.vendors[v] + "\n";

}

document.getElementById("vendors").innerText = vtxt;

}


/* SCAN PERFORMANCE */

if (data.scan_time){

document.getElementById("scan-times").innerText =
"Scan latency: " + data.scan_time + " ms";

document.getElementById("scan-latency").innerText =
"Latency: " + data.scan_time + " ms";

}

let now = new Date().toLocaleTimeString()

let consoleText =
"[ " + now + " ] RF scan complete\n" +
"[ " + now + " ] networks detected: " + wifiNetworks.length + "\n" +
"[ " + now + " ] rf density: " + data.density + "\n" +
"[ " + now + " ] strongest signal: " +
Math.max(...wifiNetworks.map(n=>n.rssi)) + " dBm\n"

document.getElementById("rf-console").innerText = consoleText

/* EVENT STREAM */

if (data.events){

document.getElementById("events").innerText =
data.events.join("\n");

}


/* NETWORK SECURITY */

if (data.security){

document.getElementById("security").innerText =
"Open networks: " + data.security.open_networks;

}


/* RF ENVIRONMENT */

if (data.environment){

document.getElementById("environment").innerText =
"Environment: " + data.environment.environment + "\n" +
"Networks detected: " + data.environment.network_count;

}
/* ---------- SYSTEM STATS ---------- */

document.getElementById("stats").innerText =
"Uptime: " + data.uptime +
" seconds | RF density: " + data.density +
"\nNetworks: " + wifiNetworks.length +
"\nCells: " + (data.cells || []).length;


/* ---------- WIFI TABLE ---------- */

let wifiHTML = `
<table>
<tr>
<th>SSID</th>
<th>Vendor</th>
<th>Signal</th>
<th>Channel</th>
<th>Band</th>
<th>Type</th>
<th>Movement</th>
</tr>
`;

for (let net of wifiNetworks){

wifiHTML += `
<tr>
<td>${net.ssid || "[Hidden]"}</td>
<td>${net.vendor || "Unknown"}</td>
<td>${net.rssi} dBm</td>
<td>${net.channel}</td>
<td>${net.band}</td>
<td>${net.device_type || "Unknown"}</td>
<td>${net.movement}</td>
</tr>
`;

}

wifiHTML += "</table>";

document.getElementById("wifi").innerHTML = wifiHTML;


/* ---------- CHANNEL USAGE ---------- */

let channelText = "";

if (data.channels){

for (let ch in data.channels){

channelText +=
"channel " + ch +
" → " + data.channels[ch] +
" networks\n";

}

}

let channelBox = document.getElementById("channels");
if (channelBox) channelBox.innerText = channelText;

/* ---------- GRAPHS ---------- */

if(data.density_timeline){
drawDensityTimeline(data.density_timeline);
}

if(data.channels){
drawChannelGraph(data.channels);
}


/* ---------- CELL TOWERS ---------- */

let cellText = "";

for (let c of (data.cells || [])){

cellText +=
"CID " + c.cid +
" | signal " + (c.dbm || c.signal) +
" dBm\n";

}

document.getElementById("cells").innerText = cellText;


/* ---------- SENSORS ---------- */

let sensorText = "";

for (let sensor in (data.sensors || {})){

if (!data.sensors[sensor].values) continue;

sensorText += sensor + " → ";
sensorText += data.sensors[sensor].values.join(", ");
sensorText += "\n";

}

document.getElementById("sensors").innerText = sensorText;


/* ---------- LAN DEVICES ---------- */

let lanBox = document.getElementById("lan");

if (lanBox){
lanBox.innerText = data.lan || "No LAN devices detected";
}


/* ---------- ALERTS ---------- */

let alerts = [];

if (data.channels){

for (let ch in data.channels){

if (data.channels[ch] >= 4){
alerts.push("Channel " + ch + " congestion detected");
}

}

}

for (let net of wifiNetworks){

if (!net.ssid){
alerts.push("Hidden network detected");
}

if (net.ssid && net.ssid.toLowerCase().includes("virus")){
alerts.push("Suspicious SSID detected: " + net.ssid);
}

}

let alertBox = document.getElementById("alerts");

if (alertBox){

if (alerts.length === 0){
alertBox.innerText = "No RF alerts";
}
else{
alertBox.innerText = alerts.join("\n");
}

}

}


/* ===============================
   RADAR DRAWING
================================ */

function drawRadar(){

ctx.clearRect(0,0,canvas.width,canvas.height);

ctx.strokeStyle = "#00ff88";
ctx.lineWidth = 1;

/* radar rings */

for (let r = 80; r <= maxRadius; r += 80){

ctx.beginPath();
ctx.arc(centerX, centerY, r, 0, Math.PI*2);
ctx.stroke();

}

/* radar cross grid */

ctx.strokeStyle = "rgba(0,255,150,0.15)"
ctx.lineWidth = 1

ctx.beginPath()
ctx.moveTo(centerX,0)
ctx.lineTo(centerX,canvas.height)
ctx.stroke()

ctx.beginPath()
ctx.moveTo(0,centerY)
ctx.lineTo(canvas.width,centerY)
ctx.stroke()

/* glowing sweep beam */

let sweepX = centerX + Math.cos(sweepAngle) * maxRadius
let sweepY = centerY + Math.sin(sweepAngle) * maxRadius

let gradient = ctx.createLinearGradient(centerX,centerY,sweepX,sweepY)

gradient.addColorStop(0,"rgba(0,255,150,0.9)")
gradient.addColorStop(1,"rgba(0,255,150,0.05)")

ctx.strokeStyle = gradient
ctx.lineWidth = 2

ctx.beginPath()
ctx.moveTo(centerX,centerY)
ctx.lineTo(sweepX,sweepY)
ctx.stroke()

sweepAngle += 0.03

/* wifi targets */

for (let net of wifiNetworks){

if (!net.rssi || !net.bssid) continue;

let angle = hashAngle(net.bssid);
let distance = rssiToDistance(net.rssi);

let x = centerX + Math.cos(angle) * distance;
let y = centerY + Math.sin(angle) * distance;


if (net.movement === "approaching"){
ctx.fillStyle = "#ff4444";
}
else if (net.movement === "leaving"){
ctx.fillStyle = "#ffaa00";
}
else if (net.movement === "new"){
ctx.fillStyle = "#00aaff";
}
else{
ctx.fillStyle = "#00ff88";
}

ctx.beginPath();

let pulse = 3 + Math.sin(Date.now()/300)*1.5

ctx.arc(x,y,pulse,0,Math.PI*2)

ctx.fill();

}

requestAnimationFrame(drawRadar);

}


/* ===============================
   START
================================ */

setInterval(updateData,5000);

updateData();
drawRadar();

