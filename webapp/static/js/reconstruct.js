$(document).ready(function() {
    // OpenStreetMap 타일 레이어를 설정합니다.
    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
  
    // 지도 객체 생성.
    const map = L.map('map', {
        center: [37.566, 126.978], // 서울의 경도, 위도.
        zoom: 12,
        layers: [osmLayer] // OpenStreetMap 타일 레이어 추가.
    });
  
    function getReconstructIconFile(reconstruct) {
        const reconstructMap = {
            "0": "1",
            "1": "2",
            "2": "3",
            "3": "4",
            "4": "5",
            "5": "6",
            "6": "7",
            "7": "8",
            "8": "9",
            "9": "10",
            "10": "11",
            "11": "12",
            "12": "13",
            "13": "14",
        };
        return reconstructMap[reconstruct] || "0";
    }
  
    function getSizeBasedOnZoom(zoom) {
        return 25 + zoom * 8; // 기본 크기 25 + 줌 레벨에 비례한 크기 증가.
    }
    
    function createIcon(url, zoom) {
        let size = getSizeBasedOnZoom(zoom);
        return L.icon({ 
            iconUrl: url, 
            iconSize: [size / 2, size / 2], 
            iconAnchor: [size / 4, size / 4], 
            popupAnchor: [0, -size / 4] 
        });
    }
  
    function addMarker(lat, lon, iconUrl, popupContent, zoomLevel) {
        const icon = createIcon(iconUrl, zoomLevel);
        const marker = L.marker([lat, lon], { icon: icon }).addTo(map);
        marker.bindPopup(popupContent);
        return marker;
    }
  
    const reconstructIconsBaseUrl = "static/icons/construct/";

    // 특정 URL에서 HTML 콘텐츠를 가져오는 함수
    async function fetchHTML(url) {
        let response = await fetch(url);
        let text = await response.text();
        return text;
    }

    // HTML 문자열을 파싱하여 DOM 객체를 반환하는 함수
    function parseHTML(html) {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, 'text/html');
        return doc;
    }

    // 특정 URL에서 HTML 콘텐츠를 가져와서 원하는 요소를 추출하는 함수
    let imgTag;
    async function getImageFromGImg(url) {
        try {
            let html = await fetchHTML(url);
            let doc = parseHTML(html);
            imgTag = doc.querySelector('g-img img');

            if (imgTag) {
                console.log('Img tag found:', imgTag);
            } else {
                console.log('No img tag found within g-img');
            }
        } catch (error) {
            console.error('Error fetching or parsing HTML:', error);
        }
    }

    // 구글에서 이미지 가져오는 것은 
    //getImageFromGImg('https://test.com/?q=test');

  
    $.getJSON('/reconstruct-data', function(data) {
        data.forEach(function(place) {
            const iconCode = getReconstructIconFile(place.cate_code);
            const iconUrl = reconstructIconsBaseUrl + iconCode + ".png";

            //getImageFromGImg(`https://www.google.com/search?q=${place.서울시_정비구역위치}&udm=2`);
            // 위도 : Latitude , 경도 : Longitude
            const popupContent = `<b>${place.재건축단계}</b><br>주소: ${place["서울시_정비구역위치"]}<br>
            사업구분: ${place["사업구분"]}<br>
                                    위도: ${place.Latitude}<br>경도: ${place.Longitude}<br>
                                    <a href='https://hogangnono.com/search?q=${place.서울시_정비구역위치}'>링크</a><br>
                                    <img src="static/icons/construct/1.png" alt="Image" style="width: 100px; height: auto; border-radius: 5px;"/>`;

            const marker = addMarker(place.Latitude, place.Longitude, iconUrl, popupContent, map.getZoom());

            // 면적을 기반으로 원을 추가 (단위: 미터)
            const area = place["정비구역면적(㎡)"] || 1000;  // 면적 값, 기본값으로 1000m² 사용
            const radius = Math.sqrt(area / Math.PI);  // 원의 반지름 = √(면적 / π)

            // 해당 위치에 원 추가
            const circle = L.circle([place.Latitude, place.Longitude], {
                color: 'blue',
                fillColor: '#30f',
                fillOpacity: 0,
                radius: radius,
                opacity: 0 // 기본적으로 원을 숨김
            //}).addTo(map).bindPopup(`<b>면적</b>: ${area}㎡<br><b>위도</b>: ${place.Latitude}<br><b>경도</b>: ${place.Longitude}`);
            }).addTo(map).bindPopup(`<b>면적</b>: ${area}㎡ 사업구분: ${place["사업구분"]}<br>`);

            // 마우스가 원에 들어갔을 때 원을 보이게 하고, 나갔을 때 원을 숨김
            circle.on('mousemove', function() {
                this.setStyle({ fillOpacity: 0.3,opacity: 1 });  // 마우스 오버 시 원을 보이게 함
            });

            circle.on('mouseout', function() {
                this.setStyle({ fillOpacity: 0,opacity: 0 });  // 마우스가 벗어날 때 원을 숨김
            });

            // 지도 줌 변경 시 아이콘 크기 조정
            map.on('zoomend', function() { 
                marker.setIcon(createIcon(iconUrl, map.getZoom()));
            });
        });
    });
});  