var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");
var buttonProcess = document.getElementById("process");
var buttonPause = document.getElementById("pause");
var statusEl = document.getElementById("status");
var downloadLink = document.getElementById("download");

function setStatus(message, type) {
    if (!statusEl) return;
    statusEl.textContent = message || "";
    statusEl.dataset.type = type || "";
}

function postJson(url, body, onSuccess) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) return;

        var rawText = xhr.responseText || "";

        if (xhr.status >= 200 && xhr.status < 300) {
            var data = null;
            try {
                data = rawText ? JSON.parse(rawText) : null;
            } catch (e) {
                data = null;
            }
            onSuccess(data, rawText);
            return;
        }

        setStatus("Có lỗi khi gọi " + url + " (" + xhr.status + ")", "error");
    };
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.send(JSON.stringify(body));
}

buttonStop.disabled = true;
buttonPause.disabled = true;
setStatus("Sẵn sàng", "success");

buttonRecord.onclick = function () {
    buttonRecord.disabled = true;
    buttonStop.disabled = false;

    if (downloadLink) {
        downloadLink.text = "";
        downloadLink.href = "";
        downloadLink.removeAttribute("download");
    }

    setStatus("Đang bắt đầu ghi hình...", "");
    postJson("/record_status", {status: "true"}, function (data, rawText) {
        if (data && data.result === "started") {
            setStatus("Đã bắt đầu ghi hình", "success");
            return;
        }
        setStatus(rawText || "Đã bắt đầu ghi hình", "success");
    });
};

buttonStop.onclick = function () {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;

    setStatus("Đang dừng ghi hình...", "");
    postJson("/record_status", {status: "false"}, function (data, rawText) {
        if (data && data.result === "stopped") {
            setStatus("Đã dừng ghi hình", "success");

            if (downloadLink && data.file_url) {
                downloadLink.text = "Tải file ghi hình";
                downloadLink.href = data.file_url;
                downloadLink.setAttribute("download", data.file_name || "video.avi");
            }
            return;
        }

        setStatus(rawText || "Đã dừng ghi hình", "success");
    });
};

buttonProcess.onclick = function () {
    buttonProcess.disabled = true;
    buttonPause.disabled = false;

    setStatus("Đang bật nhận diện...", "");
    postJson("/process_status", {status: "true"}, function (data, rawText) {
        if (data && data.result === "process") {
            setStatus("Đã bật nhận diện", "success");
            return;
        }
        setStatus(rawText || "Đã bật nhận diện", "success");
    });
};

buttonPause.onclick = function () {
    buttonProcess.disabled = false;
    buttonPause.disabled = true;

    setStatus("Đang dừng nhận diện...", "");
    postJson("/process_status", {status: "false"}, function (data, rawText) {
        if (data && data.result === "pause") {
            setStatus("Đã dừng nhận diện", "success");
            return;
        }
        setStatus(rawText || "Đã dừng nhận diện", "success");
    });
};

