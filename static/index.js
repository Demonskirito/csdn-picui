function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById("file-path").value = file.name;

        // 创建 FormData 对象，方便上传文件
        const formData = new FormData();
        formData.append('file', file);

        // 将文件上传到服务器，并获取生成的 URL
        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.url) {
                 const imgElement = document.getElementById('uploaded-image');
                 imgElement.src = data.url;
                 imgElement.style.display = 'block';  // 显示图片

                // document.querySelector(".icon").style.background = `url(${data.url})`;
                // document.querySelector(".icon").style.backgroundRepeat = "no-repeat";
                // document.querySelector(".icon").style.backgroundPosition = "center";
                // 将 URL 显示在 file-url 输入框中
                document.getElementById("file-url").value = data.url;
            } else {
                console.error("错误:", data.error);
            }
        })
        .catch(error => console.error("错误:", error));
    }
}

function copyToClipboard() {
    const fileUrlInput = document.getElementById("file-url");

    // 检查是否有内容可复制
    if (fileUrlInput.value) {
      fileUrlInput.select();
      fileUrlInput.setSelectionRange(0, 99999); // 针对移动设备

      // 执行复制操作
      document.execCommand("copy");

      // 提示复制成功
      alert("URL 已复制到剪贴板！");
    } else {
      alert("无 URL 可复制！");
    }
  }