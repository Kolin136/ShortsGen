/*
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$nav = $('#nav');

	// Breakpoints.
		breakpoints({
			wide:      [ '961px',  '1880px' ],
			normal:    [ '961px',  '1620px' ],
			narrow:    [ '961px',  '1320px' ],
			narrower:  [ '737px',  '960px'  ],
			mobile:    [ null,     '736px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

		// Toggle.
			$('<div id="headerToggle">' +
					'<a href="#header" class="toggle"></a>' +
					'</div>')
			.appendTo($body);

		// 메뉴 패널 설정
			$('#header').panel({
				delay: 500,
				hideOnClick: true,
				hideOnSwipe: true,
				resetScroll: true,
				resetForms: true,
				side: 'left',
				target: $body,
				visibleClass: 'header-visible'
			});

		// Header.
			$('#header')
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'left',
					target: $body,
					visibleClass: 'header-visible'
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


/* ///////////////// 캡셔닝 시작,결과,저장 버튼 관련 js   ////////////////////////////////////*/

let captioningResponse = null; // 캡셔닝 응답 데이터를 저장할 전역 변수
// 결과 모달 HTML 추가
const modalHTML = `
<div id="captioningResultModal" style="display: none;">  
    <div class="modal-content">
        <span class="modal-close" onclick="closeResultModal()">&times;</span>
        <div class="modal-body">
            <h2>Captioning Results</h2>
            <div id="captioningResultContent"></div>
        </div>
    </div>
</div>
`;
document.body.insertAdjacentHTML('beforeend', modalHTML);

// 결과 모달 관련 함수들
function showResultModal(data) {
	console.log('showResultModal called with data:', data);
	const modal = document.getElementById('captioningResultModal');
	console.log('modal element:', modal);
	const content = document.getElementById('captioningResultContent');
	console.log('content element:', content);

	if (!modal || !content) {
		console.error('Modal elements not found');
		return;
	}

	const formattedJson = JSON.stringify(data, null, 4);
	content.innerHTML = `<pre>${formattedJson}</pre>`;


	modal.style.display = 'block';
	requestAnimationFrame(() => {
		requestAnimationFrame(() => {
			modal.classList.add('show-modal');
		});
	});
}

function closeResultModal() {
	const modal = document.getElementById('captioningResultModal');
	modal.classList.remove('show-modal');
	setTimeout(() => {
		modal.style.display = 'none';
	}, 250);
}

// 캡셔닝 저장 함수
async function saveCaptioning() {
	if (!captioningResponse) return;

	// 확인 창 표시
	const confirmed = confirm("Do you want to save the captioning result?");

	if (confirmed) {
		try {
			const response = await fetch('http://127.0.0.1:5000/gemini/save', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(captioningResponse)
			});

			if (!response.ok) {
				throw new Error('Failed to save captioning');
			}

			alert('Captioning saved successfully!');
		} catch (error) {
			console.error('Error saving captioning:', error);
			alert('Failed to save captioning. Please try again.');
		}
	}
}


/* 비디오,프롬프트 선택한거 전역 상태 및 전역 캡셔닝 함수 */
let promptSelectedState = {
	parentElement: null,
	promptId: null,
	promptTitle: null,
	prompt: null
};

let videoSelectedState = {
	parentName: null,
	parentElement: null,
	childIndex: null,
	videoId: null,
	videoName: null
};

let isProcessing = false;

// handleCaptioning 함수 수정
async function handleCaptioning() {
	if (isProcessing || !videoSelectedState.videoId || !videoSelectedState.videoName) {
		return;
	}
	try {
		isProcessing = true;
		const captioningButton = document.getElementById('startCaptioningBtn');
		captioningButton.style.display = 'none';

		// 로딩 UI 추가
		const container = captioningButton.parentElement;
		container.innerHTML += `
            <div id="loading-spinner">
                <img src="/static/frontEnd/index/gif/duck.gif" alt="Loading..." width="150">
                <p class="processing-text">Processing...</p>
            </div>
        `;

		const formData = new FormData();
		const splitVideosData = {
			splitVideos: [{
				videoId: parseInt(videoSelectedState.videoId),
				videoName: videoSelectedState.videoName
			}]
		};
		formData.append('splitVideos', JSON.stringify(splitVideosData));
		formData.append('promptId', promptSelectedState.promptId || '');
		formData.append('prompt', promptSelectedState.prompt || '');

		const jsonFieldListForm = document.getElementById('jsonFieldListForm');
		if (jsonFieldListForm) {
			const jsonFieldListValue = jsonFieldListForm.elements['jsonFieldList'].value;
			formData.append('jsonFieldList', jsonFieldListValue);
		}

		const imageInput = document.getElementById('imageInput');
		if (imageInput.files.length > 0) {
			Array.from(imageInput.files).forEach((file, index) => {
				formData.append('images', file);
			});
		}

		const response = await fetch('http://127.0.0.1:5000/gemini/captioning', {
			method: 'POST',
			body: formData
		});

		if (!response.ok) {
			throw new Error('Failed to start captioning');
		}

		const result = await response.json();
		captioningResponse = result; // 응답 데이터 저장

		// 로딩 UI 제거 및 결과/저장 버튼 추가
		const loadingSpinner = document.getElementById('loading-spinner');
		loadingSpinner.remove();

		const buttonContainer = document.createElement('div');
		buttonContainer.id = 'captioningButtonContainer';

		const resultButton = document.createElement('button');
		resultButton.textContent = 'Captioning Result';
		resultButton.className = 'captioning-control-button result-button';
		resultButton.onclick = () => {
			console.log('Result button clicked');
			console.log('captioningResponse:', captioningResponse);
			showResultModal(captioningResponse);
		};

		const saveButton = document.createElement('button');
		saveButton.textContent = 'Captioning Save';
		saveButton.className = 'captioning-control-button save-button';
		saveButton.onclick = saveCaptioning;

		buttonContainer.appendChild(resultButton);
		buttonContainer.appendChild(saveButton);
		container.appendChild(buttonContainer);

	} catch (error) {
		console.error('Error starting captioning:', error);
		alert('Failed to start captioning process. Please try again.');

		// 에러 시 원래 버튼으로 복구
		const loadingSpinner = document.getElementById('loading-spinner');
		if (loadingSpinner) loadingSpinner.remove();
		document.getElementById('startCaptioningBtn').style.display = 'block';
	} finally {
		isProcessing = false;
	}
}

// ESC 키로 결과 모달 닫기
document.addEventListener('keydown', (e) => {
	if (e.key === 'Escape') {
		closeResultModal();
	}
});

// 모달 외부 클릭으로 닫기
window.addEventListener('click', (e) => {
	const modal = document.getElementById('captioningResultModal');  // ID 수정
	if (e.target === modal) {
		closeResultModal();
	}
});

//       /////////////////////////////        프롬프트 리스트 관련 js       //////////////////////////////////////////////////

// 프롬프트 목록 로딩
document.addEventListener('DOMContentLoaded', async () => {
	const promptListContainer = document.getElementById('promptListContainer');
	const promptModal = document.getElementById('promptModal');
	const promptCloseButton = document.querySelector('.prompt-close-button');
	let selectedState = {
		parentElement: null,
		promptId: null,
		promptTitle: null,
		prompt: null
	};

	const closePromptModal = () => {
		promptModal.classList.remove('show-prompt-modal');
		setTimeout(() => {
			promptModal.style.display = 'none';
		}, 250);
	};

	const openPromptModal = (prompt, articleElement) => {
		document.getElementById('promptModalTitle').textContent = prompt.prompt_title;

		const modalBody = document.createElement('div');
		modalBody.className = 'prompt-modal-body';

		const buttonContainer = document.createElement('div');
		buttonContainer.className = 'prompt-button-container';

		const selectButton = document.createElement('button');
		selectButton.textContent = 'Select';
		selectButton.className = 'prompt-select-button';

		selectButton.onclick = () => {
			if (selectedState.parentElement) {
				selectedState.parentElement.classList.remove('prompt-selected');
			}
			articleElement.classList.add('prompt-selected');

			selectedState = {
				parentElement: articleElement,
				promptId: prompt.prompt_id,
				promptTitle: prompt.prompt_title,
				prompt: prompt.prompt_text
			};

			promptSelectedState = selectedState;

			closePromptModal();
		};

		buttonContainer.appendChild(selectButton);

		modalBody.innerHTML = `
            <p><strong>Creation date:</strong> ${new Date(prompt.created_at).toLocaleString()}</p>
            <p><strong>Modification date:</strong> ${new Date(prompt.updated_at).toLocaleString()}</p>
            <p><strong>prompt content:</strong></p>
            <div class="prompt-content">${prompt.prompt_text}</div>
        `;

		const modalContent = promptModal.querySelector('.prompt-modal-content');
		const existingBody = promptModal.querySelector('.prompt-modal-body');
		if (existingBody) {
			existingBody.remove();
		}
		modalContent.appendChild(buttonContainer);
		modalContent.appendChild(modalBody);

		promptModal.style.display = 'block';
		setTimeout(() => {
			promptModal.classList.add('show-prompt-modal');
		}, 10);
	};

	promptCloseButton.addEventListener('click', closePromptModal);

	window.addEventListener('click', (e) => {
		if (e.target === promptModal) {
			closePromptModal();
		}
	});

	document.addEventListener('keydown', (e) => {
		if (e.key === 'Escape' && promptModal.style.display === 'block') {
			closePromptModal();
		}
	});

	try {
		const response = await fetch('http://127.0.0.1:5000/prompt/search');
		const data = await response.json();

		const colDiv = document.createElement('div');
		colDiv.className = 'col-12';

		const flexContainer = document.createElement('div');
		flexContainer.style.display = 'flex';
		flexContainer.style.flexWrap = 'wrap';
		flexContainer.style.gap = '20px';
		flexContainer.style.justifyContent = 'flex-start';

		data.prompts.forEach(prompt => {
			const article = document.createElement('article');
			article.className = 'promptListItem';
			article.style.width = 'calc(25% - 15px)';
			article.style.marginBottom = '20px';
			article.style.cursor = 'pointer';

			article.innerHTML = `
                <header>
                    <h3>${prompt.prompt_title}</h3>
                </header>
            `;

			article.addEventListener('click', () => {
				openPromptModal(prompt, article);
			});

			flexContainer.appendChild(article);
		});

		colDiv.appendChild(flexContainer);
		promptListContainer.appendChild(colDiv);

	} catch (error) {
		console.error('Failed to load prompt list:', error);
	}
});



//       /////////////////////////////        비디오 리스트 관련 js       //////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', async () => {
	const videoListContainer = document.querySelector('#contact .container');
	const videoModalHTML = `
        <div id="videoSplitModal" class="video-split-modal">
            <div class="video-split-modal-content">
                <span class="video-split-close">&times;</span>
                <div class="video-split-modal-body"></div>
            </div>
        </div>
    `;

	let selectedState = {
		parentName: null,
		parentElement: null,
		childIndex: null,
		videoId: null,
		videoName: null
	};

	document.body.insertAdjacentHTML('beforeend', videoModalHTML);

	const videoModal = document.getElementById('videoSplitModal');
	const videoCloseButton = document.querySelector('.video-split-close');
	const captioningButton = document.getElementById('startCaptioningBtn');

	const deselectParent = (element) => {
		if (element) {
			element.classList.remove('video-parent-selected');
		}
	};

	const selectParent = (element) => {
		if (element) {
			element.classList.add('video-parent-selected');
		}
	};

	const closeVideoSplitModal = () => {
		videoModal.classList.remove('show-video-modal');
		setTimeout(() => {
			videoModal.style.display = 'none';
			if (selectedState.parentElement && selectedState.childIndex !== null) {
				selectParent(selectedState.parentElement);
			}
		}, 250);
	};

	const openVideoSplitModal = async (originalVideoName, parentElement) => {
		try {
			const response = await fetch(`http://127.0.0.1:5000/video/split/${originalVideoName}`);
			const data = await response.json();

			const modalBody = videoModal.querySelector('.video-split-modal-body');
			modalBody.innerHTML = `
                <h2>Split Videos - ${originalVideoName}</h2>
                <div class="video-split-list">
                    ${data.splitVideos.map((video, index) => `
                        <div class="video-split-list-item">
                            <label>
                                <input type="radio" 
                                    name="videoSplitSelect" 
                                    data-video-id="${video.videoId}"
                                    data-video-name="${video.videoName}"
                                    ${selectedState.parentName === originalVideoName && selectedState.childIndex === index ? 'checked' : ''}>
                                <span class="video-name">${video.videoName}</span>
                            </label>
                        </div>
                    `).join('')}
                </div>
            `;

			if (selectedState.parentName === originalVideoName && selectedState.childIndex !== null) {
				const items = modalBody.querySelectorAll('.video-split-list-item');
				items[selectedState.childIndex].classList.add('video-selected');
			}

			modalBody.querySelectorAll('input[type="radio"]').forEach((radio, index) => {
				radio.addEventListener('change', (e) => {
					if (e.target.checked) {
						if (originalVideoName !== selectedState.parentName) {
							deselectParent(selectedState.parentElement);
						}
						modalBody.querySelectorAll('.video-split-list-item').forEach(item => {
							item.classList.remove('video-selected');
						});

						const selectedItem = e.target.closest('.video-split-list-item');
						selectedItem.classList.add('video-selected');

						selectedState = {
							parentName: originalVideoName,
							parentElement: parentElement,
							childIndex: index,
							videoId: e.target.dataset.videoId,
							videoName: e.target.dataset.videoName
						};

						videoSelectedState = selectedState;

						selectParent(parentElement);
						captioningButton.disabled = false;
					}
				});
			});

			videoModal.style.display = 'block';
			setTimeout(() => {
				videoModal.classList.add('show-video-modal');
			}, 10);

		} catch (error) {
			console.error('Failed to load split videos:', error);
			alert('Failed to load split videos');
		}
	};

	try {
		const response = await fetch('http://127.0.0.1:5000/video/original');
		const data = await response.json();

		const colDiv = document.createElement('div');
		colDiv.className = 'col-12';

		const flexContainer = document.createElement('div');
		flexContainer.className = 'video-list-container';

		data.fileList.forEach(filename => {
			const article = document.createElement('article');
			article.className = 'video-list-item';
			article.setAttribute('data-video-name', filename);

			article.innerHTML = `
                <header>
                    <h3>${filename}</h3>
                </header>
            `;

			article.addEventListener('click', () => {
				openVideoSplitModal(filename, article);
			});

			flexContainer.appendChild(article);
		});

		colDiv.appendChild(flexContainer);
		videoListContainer.appendChild(colDiv);

	} catch (error) {
		console.error('Failed to load video list:', error);
	}

	captioningButton.addEventListener('click', handleCaptioning);
	videoCloseButton.addEventListener('click', closeVideoSplitModal);

	window.addEventListener('click', (e) => {
		if (e.target === videoModal) {
			closeVideoSplitModal();
		}
	});

	document.addEventListener('keydown', (e) => {
		if (e.key === 'Escape' && videoModal.style.display === 'block') {
			closeVideoSplitModal();
		}
	});
});



// 이미지 미리보기 및 제거 기능을 위한 이벤트 리스너 추가
document.addEventListener('DOMContentLoaded', () => {
	const imageInput = document.getElementById('imageInput');
	const selectedImagesContainer = document.getElementById('selectedImages');

	imageInput.addEventListener('change', (e) => {
		selectedImagesContainer.innerHTML = '';
		Array.from(e.target.files).forEach((file, index) => {
			const reader = new FileReader();
			reader.onload = (event) => {
				const div = document.createElement('div');
				div.className = 'selected-image-item';
				div.innerHTML = `
                    <img src="${event.target.result}" alt="Selected image ${index + 1}">
                    <button class="remove-image" onclick="removeImage(${index})">×</button>
                `;
				selectedImagesContainer.appendChild(div);
			};
			reader.readAsDataURL(file);
		});
	});
});

function removeImage(index) {
	const imageInput = document.getElementById('imageInput');
	const dataTransfer = new DataTransfer();

	Array.from(imageInput.files)
	.filter((_, i) => i !== index)
	.forEach(file => dataTransfer.items.add(file));

	imageInput.files = dataTransfer.files;

	// 미리보기 업데이트
	const event = new Event('change');
	imageInput.dispatchEvent(event);
}


/* ////////////////////// 이전 캡셔닝 데이터 조회 관련 js /////////////////////////////   */
/* ////////////////////// 이전 캡셔닝 데이터 조회 관련 js /////////////////////////////   */

// 이전 캡셔닝 모달 HTML 추가
const previousModalHTML = `
<div id="previousCaptioningModal" style="display: none;">
   <div class="modal-content">
       <span class="modal-close" onclick="closePreviousModal()">&times;</span>
       <div class="modal-body">
           <h2>Previous Captioning Results</h2>
           <div id="previousCaptioningContent"></div>
       </div>
   </div>
</div>
`;
document.body.insertAdjacentHTML('beforeend', previousModalHTML);

// 버튼 상태 업데이트 함수
function checkPreviousCaptioningButton() {
	const viewPreviousButton = document.getElementById('viewPreviousCaptioningBtn');
	if (viewPreviousButton) {
		viewPreviousButton.disabled = !videoSelectedState.videoId || !promptSelectedState.promptId;
	}
}

// 이전 캡셔닝 조회 처리 함수
async function handleViewPreviousCaptioning() {
	if (!videoSelectedState.videoId || !promptSelectedState.promptId) {
		return;
	}

	try {
		const response = await fetch(
				`http://127.0.0.1:5000/gemini/captioning/video/${videoSelectedState.videoId}/prompt/${promptSelectedState.promptId}`
		);

		if (!response.ok) {
			throw new Error('Failed to fetch previous captioning');
		}

		const result = await response.json();
		showPreviousModal(result);
	} catch (error) {
		console.error('Error fetching previous captioning:', error);
		alert('Failed to fetch previous captioning results. Please try again.');
	}
}

// 이전 캡셔닝 모달 표시 함수
function showPreviousModal(data) {
	const modal = document.getElementById('previousCaptioningModal');
	const content = document.getElementById('previousCaptioningContent');
	const formattedJson = JSON.stringify(data, null, 4);
	content.innerHTML = `<pre>${formattedJson}</pre>`;
	modal.style.display = 'block';
	requestAnimationFrame(() => {
		requestAnimationFrame(() => {
			modal.classList.add('show-modal');
		});
	});
}

// 이전 캡셔닝 모달 닫기 함수
function closePreviousModal() {
	const modal = document.getElementById('previousCaptioningModal');
	modal.classList.remove('show-modal');
	setTimeout(() => {
		modal.style.display = 'none';
	}, 250);
}

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', () => {
	// 이전 캡셔닝 버튼 생성 및 추가
	const previousSection = document.querySelector('section.three .container');
	const button = document.createElement('button');
	button.id = 'viewPreviousCaptioningBtn';
	button.className = 'previous-captioning-button';
	button.textContent = 'View Previous Captioning';
	button.disabled = true;
	button.addEventListener('click', handleViewPreviousCaptioning);
	previousSection.appendChild(button);

	// 프롬프트 선택 변경 감지
	document.addEventListener('click', function(e) {
		if(e.target && e.target.classList.contains('prompt-select-button')) {
			setTimeout(checkPreviousCaptioningButton, 100);
		}
	});

	// 비디오 선택 변경 감지
	document.addEventListener('change', function(e) {
		if(e.target && e.target.name === 'videoSplitSelect') {
			setTimeout(checkPreviousCaptioningButton, 100);
		}
	});
});

// ESC 키로 모달 닫기
document.addEventListener('keydown', (e) => {
	if (e.key === 'Escape') {
		closePreviousModal();
	}
});

// 모달 외부 클릭으로 닫기
window.addEventListener('click', (e) => {
	const modal = document.getElementById('previousCaptioningModal');
	if (e.target === modal) {
		closePreviousModal();
	}
});