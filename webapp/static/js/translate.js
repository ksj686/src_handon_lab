// 번역 데이터를 담을 객체
let translations = {};

// 기본 언어 (영어)로 시작
let currentLang = 'en';

// 번역 데이터를 로드하는 함수
function loadTranslations(lang) {
  fetch(`static/locales/${lang}/translation.json`)
    .then(response => response.json())
    .then(data => {
      translations = data;
      currentLang = lang;
      updateContent();
    })
    .catch(error => console.error('Error loading translations:', error));
}

// 페이지의 콘텐츠를 업데이트하는 함수
function updateContent() {
  document.getElementById('welcome').textContent = translations.welcome;
  document.getElementById('greeting').textContent = translations.greeting;
}

// 언어 변경 함수
function changeLanguage(lang) {
  loadTranslations(lang);
}

// 페이지가 로드될 때 기본 언어(영어)로 번역 데이터를 로드
window.onload = function() {
  loadTranslations('en');
};

