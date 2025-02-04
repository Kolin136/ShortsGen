/*
	Full Motion by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

(function($) {

	skel.breakpoints({
		xlarge: '(max-width: 1680px)',
		large: '(max-width: 1280px)',
		medium: '(max-width: 980px)',
		small: '(max-width: 736px)',
		xsmall: '(max-width: 480px)'
	});

	$(function() {

		var $window = $(window),
				$body = $('body');

		// Disable animations/transitions until the page has loaded.
		$body.addClass('is-loading');

		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-loading');
			}, 100);
		});

		// Fix: Placeholder polyfill.
		$('form').placeholder();

		// Banner.
		var $banner = $('#banner');

		if ($banner.length > 0) {
			if (skel.vars.IEVersion < 12) {
				$window.on('resize', function() {
					var wh = $window.height() * 0.60,
							bh = $banner.height();

					$banner.css('height', 'auto');

					window.setTimeout(function() {
						if (bh < wh)
							$banner.css('height', wh + 'px');
					}, 0);
				});

				$window.on('load', function() {
					$window.triggerHandler('resize');
				});
			}

			var video = $banner.data('video');

			if (video)
				$window.on('load.banner', function() {
					$window.off('load.banner');
					if (!skel.vars.mobile && !skel.breakpoint('large').active && skel.vars.IEVersion > 9)
						$banner.append('<video autoplay loop><source src="' + video + '.mp4" type="video/mp4"><source src="' + video + '.webm" type="video/webm"></video>');
				});

			$banner.find('.more').addClass('scrolly');
		}

		$('.scrolly').scrolly();

		var videoContainer = $('.thumbnails');

		fetch('http://127.0.0.1:5000/video/merge', {
			method: 'GET'
		})
		.then(response => response.json())
		.then(data => {
			var videoList = data.file_url;
			videoContainer.empty();

			videoList.forEach(videoData => {
				var videoUrl = videoData.video_url;
				var thumbnailUrl = videoData.thumbnail_url;  // 썸네일 URL 가져오기
				var videoFileName = decodeURIComponent(videoUrl.split('/').pop().split('.')[0]);

				// 버튼 스타일을 랜덤으로 선택 (style2, style3, 기본 스타일)
				var buttonStyles = ["", "style2", "style3"];
				var randomStyle = buttonStyles[Math.floor(Math.random() * buttonStyles.length)];

				var boxHtml = `
            <div class="box">
                <a href="${videoUrl}" class="image fit" data-poptrox="iframe,800x450">
                    <img src="${thumbnailUrl}" alt="썸네일 이미지" width="600" height="338">
                </a>
                <div class="inner">
                    <h3>비디오</h3>
                    <p>${videoFileName}</p>
                    <a href="${videoUrl}"  class="button ${randomStyle} fit" data-poptrox="iframe,800x450">Watch</a>
                </div>
            </div>
        `;

				videoContainer.append(boxHtml);
			});

			// 여기서 바로 poptrox 초기화
			$('.thumbnails').poptrox({
				onPopupClose: function() { $body.removeClass('is-covered'); },
				onPopupOpen: function() { $body.addClass('is-covered'); },
				baseZIndex: 10001,
				useBodyOverflow: false,
				overlayColor: '#222226',
				overlayOpacity: 0.75,
				popupLoaderText: '',
				fadeSpeed: 500,
				usePopupDefaultStyling: false,
				windowMargin: (skel.breakpoint('small').active ? 5 : 50)
			});
		})
		.catch(error => console.error('비디오 데이터를 불러오는데 실패했습니다.', error));

		$window.on('load', function() {
			$window.trigger('scroll');
		});

	});

})(jQuery);



// 왼쪽 메뉴판에 현재 페이지와 일치하는 메뉴 항목 강조
document.addEventListener("DOMContentLoaded", () => {
	const currentPath = window.location.pathname; // 현재 URL의 경로

	// 메뉴 항목들을 선택
	const menuItems = document.querySelectorAll("#nav ul li a");

	menuItems.forEach((menuItem) => {
		if (menuItem.getAttribute("href") === currentPath) {
			menuItem.classList.add("active"); // 현재 페이지와 일치하는 메뉴에 active 추가
		}
	});
});



