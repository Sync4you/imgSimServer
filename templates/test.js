         fetch('/get').then(response => response.json())
                .then(data => {
                    const param = data.param;
                    console.log("从Flask获取的参数：", param.id);
                })
                .catch(error => console.error("获取参数失败：", error));