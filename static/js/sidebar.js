const outContent = $('.out-content')[0]
const sidebarList = $('#sidebar-list')[0]
const upfileBt = $('.upfile-bt')[0]



$('#display').click(function(){

  if( outContent.style.display == "none" || outContent.style.display == ""){
    
    outContent.style.display = "block"
  }else{
    outContent.style.display = "none"
  }
  
})


$(function () {
  download()


  $("#btn_uploadimg").click(function () {
   
  })
})
function uploadFile() {

  var fileObj = document.getElementById("FileUpload").files[0]; // js 获取文件对象
  if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
      
      return;
  }
  var formFile = new FormData();
  formFile.append("action", "UploadVMKImagePath");  
  formFile.append("file", fileObj); //加入文件对象

  var data = formFile;
  $.ajax({
      url: `http://${document.domain}:${location.port}/upload`,
      data: data,
      type: "Post",
      dataType: "json",
      cache: false,//上传文件无需缓存
      processData: false,//用于对data参数进行序列化处理 这里必须false
      contentType: false, //必须
      success: function (result) {
          alert("上传完成!");
          download()
      },
  })
}
setInterval(function(){
download()
},5000)
function download() {
  sidebarList.innerHTML = ""
  $.ajax({
    url: "http://192.168.10.14:5000/loadfile",
    type: "POST",
    success: function(res){
      let  data = res.data.split(',')
        for(item in data) {
          sidebarList.innerHTML += `
          <li><a href="http://${document.domain}:${location.port}/download/${data[item]}" download="${data[item]}">${data[item]}</a></li>
          `
        }
    }
  })
}
