var MainFormLogic = {
    GetLink: function () {
        var linkValue = document.getElementById("linkInput").value;

        var data = new FormData();
        data.append("link", linkValue);

        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;

        xhr.addEventListener("readystatechange", function () {
            if (this.readyState === 4) {
                var resultBlock = document.getElementById("shortLinkResult");

                var resultLink = document.querySelector("#shortLinkResult > a");
                resultLink.href = this.responseText;
                resultLink.innerHTML = this.responseText;

                resultBlock.className = "show-element";
            }
        });

        xhr.open("POST", "/short_link");

        xhr.send(data);
    },

    DisplayLinkBtn : function () {
        var btn = document.getElementById("getlnkBtn");
        var linkValue = document.getElementById("linkInput").value;

        if(linkValue.length) {
            btn.className = "getlnk-btn show-element";
        }
        else {
            btn.className = "getlnk-btn";
        }

    }
}