// $( document ).ready(function() {
// $('.answer').hide();
// $('.ques').hide();
// $('.click').click(function() {
// $('.answer').show();
// });
// });
// var xmlhttp;
// function load(url,cfunc) {
// xmlhttp = new XMLHttpRequest();
// xmlhttp.onreadystatechange = cfunc;
// xmlhttp.open("GET",url,true);
// xmlhttp.send();
// }
// function my()
// {
// load("/test",function()
// {
// if (xmlhttp.readyState == 4 && xmlhttp.status = 200)
// {
// document.getElementById("mydiv").innerHTML = xmlhttp.responseText;
// }
// });
// }


function update() {
holder = $("#mydiv")
$.getJSON("/test/",
function(data) {
jQuery.each(data,function() {
//holder.prepend('<p>'+this.pk+'</p>');
//holder.prepend('<p>'+this.fields.content+'</p>');
holder.prepend('<p>'+this.fields.content+'</p>');
});
})
};
$(document).ready(function(){
setInterval("update()",6000);
});