/*
*	Cbox dynamic loader v.2
*/
(function () {
	var showByDefault = true;
	var cboxContainer = document.getElementById("cboxwrap");
	var cboxToggleButton = document.getElementById("cboxbutton");
	var buttonStringOpen = "Open Cbox";
	var buttonStringClose = "Close Cbox";
	var lsKey = "cbox:isOpen";

	var cboxHTML = '<!-- BEGIN CBOX - www.cbox.ws - v4.1 -->'
	+'<div id="cboxdiv" style="position: relative; margin: 0 auto; width: 250px; font-size: 0; line-height: 0;">'
	+'<div style="position: relative; height: 300px; overflow: auto; overflow-y: auto; -webkit-overflow-scrolling: touch; border:#F6F3E0 1px solid;"><iframe src="http://www2.cbox.ws/box/?boxid=1800297&boxtag=wt70by&sec=main" marginheight="0" marginwidth="0" frameborder="0" width="100%" height="100%" scrolling="auto" allowtransparency="yes" name="cboxmain2-1800297" id="cboxmain2-1800297"></iframe></div>'
	+'<div style="position: relative; height: 90px; overflow: hidden; border:#F6F3E0 1px solid; border-top: 0px;"><iframe src="http://www2.cbox.ws/box/?boxid=1800297&boxtag=wt70by&sec=form" marginheight="0" marginwidth="0" frameborder="0" width="100%" height="100%" scrolling="no" allowtransparency="yes" name="cboxform2-1800297" id="cboxform2-1800297"></iframe></div>'
	+'</div>'
	+'<!-- END CBOX -->';

	var htmlInjected = false;
	var isVisible = false;
	var toggleCbox = function (show) {
		
		if (!show) {
			cboxContainer.style.display = "none";
			if (cboxToggleButton) {
				cboxToggleButton.innerHTML = buttonStringOpen;
			}
			
		}
		else {
			cboxContainer.style.display = "block";
			if (cboxToggleButton) {
				cboxToggleButton.innerHTML = buttonStringClose;
			}
		}
		
		if (show && !htmlInjected) {
			cboxContainer.innerHTML = cboxHTML;
			htmlInjected = true;
		}
		
		isVisible = show;
	}

	if (localStorage && lsKey && typeof localStorage.getItem(lsKey) === "string") {
		toggleCbox((localStorage.getItem(lsKey) === "yes"));
	}
	else {
		toggleCbox(showByDefault);
	}

	if (cboxToggleButton) {
		cboxToggleButton.onclick = function () {
			toggleCbox(!isVisible);
			
			if (localStorage && lsKey) {
				localStorage.setItem(lsKey, isVisible ? "yes" : "no");
			}
		}
	}
})();

