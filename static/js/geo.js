
var tmGeo = function() {

  var resultCallback = null;

  // Private Methods
  var handleResults = function(position) {
    resultCallback(position.coords.latitude, position.coords.longitude);
  }
  
  var handleErrors = function(error) {
            switch(error.code) {  
            case error.PERMISSION_DENIED: 
              alert("user did not share geolocation data");  
              break;  
  
            case error.POSITION_UNAVAILABLE: alert("could not detect current position");  
              break;  
  
            case error.TIMEOUT: alert("retrieving position timed out");  
              break;  
  
            default: alert("unknown error");  
              break;  
            }  
  }
  
        function handle_geolocation_query(position) {  
          handleResults(position);
        }  

  // Public Interface
  return {
    getCurrentLocation: function (callback) {  
      resultCallback = callback;
      navigator.geolocation.getCurrentPosition(handleResults, handleErrors);  
    }
  }

}  
          
  
