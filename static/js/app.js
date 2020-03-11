console.log("please dear god!");
console.log("please");


 $('#textFile').on("change",function() {
      console.log("change fire");
     var i = $(this).prev('label').clone();
      var file = $('#textFile')[0].files[0].name;
   console.log(file);
      $(this).prev('label').text(file);
});