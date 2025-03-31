$(document).ready(function() {
  // 지도를 생성하고 중심을 설정합니다.
  let map = L.map('map').setView([36.5, 127.5], 10);

  // OpenStreetMap 타일을 추가합니다.
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  
	//let weatherIconsBaseUrl = "http://openweathermap.org/img/wn/";
  let weatherIconsBaseUrl = "static/icons/animated/";

	function getWeatherIconCode(weather) {
        let weatherMap = {
            "clearday": "01d",
            "clearnight": "01n",
            "pcloudyday": "02d",
            "pcloudynight": "02n",
            "mcloudyday": "03d",
            "mcloudynight": "03n",
            "cloudyday": "04d",
            "cloudynight": "04n",
            "rain": "10d",
            "snow": "13d"
        };
        return weatherMap[weather] || "01d";
    }

    function getWeatherIconFile(weather) {
      let weatherMap = {
          "clearday": "day",
          "clearnight": "night",
          "pcloudyday": "cloudy-day-1",
          "pcloudynight": "cloudy-night-1",
          "mcloudyday": "cloudy-day-2",
          "mcloudynight": "cloudy-night-2",
          "cloudyday": "cloudy-day-3",
          "cloudynight": "cloudy-night-3",
          "rain": "rainy-1",
          "snow": "snowy-1"
      };
      return weatherMap[weather] || "day";
  }

  function getSizeBasedOnZoom(zoom) { 
    return 25 + zoom * 8; // 예: 기본 크기 25 + 줌 레벨에 비례한 크기 증가 
  }
	
  function createIcon(url, zoom) { 
    let size = getSizeBasedOnZoom(zoom); 
    return L.icon({ 
      iconUrl: url, 
      iconSize: [size, size], 
      iconAnchor: [size / 2, size / 2], 
      popupAnchor: [0, -size / 2] 
    }); 
  }
  
  // 날씨 데이터를 가져와서 마커를 추가합니다.
  $.getJSON('/weather-data', function(data) {
      data.forEach(function(city) {
			//let iconCode = getWeatherIconCode(city.weather.weather);
      let iconCode = getWeatherIconFile(city.weather.weather);
      //let iconUrl = weatherIconsBaseUrl + iconCode + "@2x.png";
      let iconUrl = weatherIconsBaseUrl + iconCode + ".svg";

      /*
      let icon = L.icon({
          iconUrl: iconUrl,
          iconSize: [100, 100],
          iconAnchor: [25, 25],
          popupAnchor: [0, -25]
      });
      */

      let marker = L.marker([city.lat, city.lon], { icon: createIcon(iconUrl, map.getZoom()) }).addTo(map);
      let popupContent = `<b>${city.name}</b><br>Temperature: ${city.weather.temp2m}°C<br>Weather: ${city.weather.weather}`;
      marker.bindPopup(popupContent);

      map.on('zoomend', function() { 
        marker.setIcon(createIcon(iconUrl, map.getZoom())); 
      });
  });
  });
});
