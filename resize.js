//<![CDATA[
$(document).ready(function(){
 var wi=$(window).width();
 var w=$(window).width()+300;

 $(window).resize(function(){
  //alert($(window).width());
  function(){
   if(w <= 1024)
   {
    alert('a');
   }
   else
   {
    alert('b');
   }
  } 
  /*
  if($(window).width()<1024)
  {
   alert($(window).width());
   $('.chrome').width(w);
  }
 });
 */
 //$('.chrome').width($(window).width());
}); 
//]]>