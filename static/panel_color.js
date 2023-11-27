$(document).ready(function(){
  
    var mc = {
      '7-9'     : 'red',
      '3-6'    : 'yellow',
      '0-2'   : 'green'
    };
    
  function between(x, min, max) {
    return x >= min && x <= max;
  }
    
  
    
    var dc;
    var first; 
    var second;
    var th;
    
    $('th').each(function(index){
      
      th = $(this);
      
      dc = parseInt($(this).attr('data-color'),10);
      
      
        $.each(mc, function(name, value){
          
          
          first = parseInt(name.split('-')[0],10);
          second = parseInt(name.split('-')[1],10);
          
          console.log(between(dc, first, second));
          
          if( between(dc, first, second) ){
            th.addClass(value);
          }
  
      
      
        });
      
    });
  });

  // https://jsbin.com/kujekijiqe/edit?html,js,output
  // https://stackoverflow.com/questions/31803300/coloring-the-text-depending-on-numeric-value-using-css