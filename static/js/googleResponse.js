function googleResponse(data) {
	
    transcript = document.getElementById("transcript");
    
    transcript.style.display = "block";
    content = document.getElementById("string");
    content.innerHTML = "\"" + (data.transcript).substr(2,data.transcript.length-3) + "\"";
    console.log(data.transcript);
    confidence = document.getElementById("confidence");

    confidence.innerHTML = "Confidence.    " + data.confidence;
    confidence.style.display = "block";
    div = document.getElementById("recordingDiv");
    div.style.display = "none";

}