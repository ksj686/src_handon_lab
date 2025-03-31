const API_KEY='uRV1Pn8Vwx5a2SZ2b%2FH5e%2FSaeB%2BDKvNMktskQjlg5vk8mrJGUg2HiUUjJAZYMtEyYQRdOTtz%2Bs5GPnvC414gAQ%3D%3D';

async function getData(){
    const url=`http://apis.data.go.kr/B552061/frequentzoneBicycle/getRestFrequentzoneBicycle?ServiceKey=${API_KEY}&searchYearCd=2015&siDo=11&guGun=680&type=json&numOfRows=20&pageNo=1`;
    const response = await fetch(url);
    const data = await response.json();
    console.log("data",data);
    const locations = data.items.item.map((spot)=>[
        spot.spot_nm,
        spot.la_crd,
        spot.lo_crd,
    ]);
    console.log("locations",locations);
    drawMap(locations);
}

function drawMap(locations) {
    // locations = [["지역이름",위도,경도],
    //              ["지역이름",위도,경도]
    //             ]

    // 맵 생성
    const map = L.map('map').setView([locations[0][1], locations[0][2]], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    locations.forEach((location) => {
        const marker = L.marker([location[1], location[2]]).addTo(map);
        marker.bindPopup(location[0]);
    });
}

getData();

/*
function drawMap(locations) {
    // 매겨변수 형태
    // locations = [["지역이름",위도,경도],
    //                ["지역이름",위도,경도]
    //            ]
    

    // 맵 생성
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 13,
      center: new google.maps.LatLng(locations[0][1], locations[0][2]),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    });
  
    const infowindow = new google.maps.InfoWindow();
  
    let marker, i;
  
    for (i = 0; i < locations.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map,
      });
  
      google.maps.event.addListener(
        marker,
        "click",
        (function (marker, i) {
          return function () {
            infowindow.setContent(locations[i][0]);
            infowindow.open(map, marker);
          };
        })(marker, i)
      );
    }
  }
*/