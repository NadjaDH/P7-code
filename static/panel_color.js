$(document).ready(function(){
    // a variable that gives an output depending on an integer

    var mc = {
      '7-9'     : '#F16B5C',
      '3-6'    : 'yellow',
      '0-2'   : '#B3D93A'
    };
    
  // a function to limit the integer to the given values
  function between(x, min, max) {
    return x >= min && x <= max;
  }
    
  
    
    var dc;
    var first; 
    var second;
    var th;
  // this applies the code to all instances of table headers 'th'  
    $('th').each(function(index){
      
      th = $(this);
      // makes the code work on 'data-color' tagged elements
      dc = parseInt($(this).attr('data-color'),10);
      
      // makes the code react to values and act according to the strings in mc
        $.each(mc, function(name, value){
          
          // sets upper and lower limit for the value range
          first = parseInt(name.split('-')[0],10);
          second = parseInt(name.split('-')[1],10);
          
          console.log(between(dc, first, second));
          // if the value is in the given range apply it to the background
          if( between(dc, first, second) ){
            th.css('background-color', value);
          }
  
      
      
        });
      
    });
  });

  // https://jsbin.com/kujekijiqe/edit?html,js,output
  // https://stackoverflow.com/questions/31803300/coloring-the-text-depending-on-numeric-value-using-css