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


/* ///////////////// 크로마 DB 저장 관련 js   ////////////////////////////////////*/

/* 프롬프트 선택한거 전역 상태 */
let promptSelectedState = {
	parentElement: null,
	promptId: null,
	promptTitle: null,
	prompt: null
};

// 크로마 DB 저장 함수
async function handleChromaSave() {
	try {
		if (!promptSelectedState.promptId) {
			return;
		}

		// collection name 가져오기
		const collectionNameTextarea = document.querySelector('#collectionNameForm textarea[name="collectionName"]');
		const collectionName = collectionNameTextarea.value.trim();

		// Collection name 유효성 검사
		const namePattern = /^[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]$/;

		if (!collectionName) {
			alert('Please enter a collection name');
			return;
		}

		if (collectionName.length < 3 || collectionName.length > 63) {
			alert('Collection name must be between 3 and 63 characters');
			return;
		}

		if (!namePattern.test(collectionName)) {
			alert('Collection name must:\n\n' +
					'- Start and end with an alphanumeric character\n' +
					'- Contain only alphanumeric characters, underscores, or hyphens\n' +
					'- Not contain any special characters or spaces');
			return;
		}

		const response = await fetch('http://127.0.0.1:5000/chroma/save', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				promptId: promptSelectedState.promptId,
				collectionName: collectionName
			})
		});

		const data = await response.json();

		if (response.status === 404) {
			alert("This prompt has no captioned data. Please proceed with captioning first");
			return;
		}

		if (!response.ok) {
			throw new Error('Failed to save to Chroma DB');
		}

		alert('Successfully saved to Chroma DB');

	} catch (error) {
		console.error('Error saving to Chroma DB:', error);
		alert('Failed to save to Chroma DB. Please try again.');
	}
}

// DOM이 로드되면 버튼 초기 상태 설정
document.addEventListener('DOMContentLoaded', () => {
	const saveButton = document.getElementById('saveToChromaBtn');
	saveButton.disabled = true; // 초기에는 비활성화
	saveButton.addEventListener('click', handleChromaSave);
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

	const openPromptModal = async (prompt, articleElement) => {
		document.getElementById('promptModalTitle').textContent = prompt.prompt_title;

		const modalBody = document.createElement('div');
		modalBody.className = 'prompt-modal-body';

		// Collection info container
		const collectionInfoContainer = document.createElement('div');
		collectionInfoContainer.className = 'collection-info-container';

		// Collection view button and initial status
		const collectionViewButton = document.createElement('button');
		collectionViewButton.textContent = 'View Collection';
		collectionViewButton.className = 'collection-view-button';

		const collectionStatus = document.createElement('span');
		collectionStatus.className = 'collection-status';
		collectionStatus.textContent = 'Click to check collection name'; // 초기 상태 텍스트

		// View Collection 버튼 클릭 이벤트
		collectionViewButton.onclick = async () => {
			try {
				const response = await fetch(`http://127.0.0.1:5000/gemini/captioning/prompt/${prompt.prompt_id}`);
				const data = await response.json();

				if (data.collectionName && data.collectionName.trim()) {
					collectionStatus.textContent = data.collectionName;
				}
				else if(response.status === 404)  {
					collectionStatus.textContent = 'No collection currently exists for this prompt';
				}
			} catch (error) {
				collectionStatus.textContent = 'No collection currently exists for this prompt';
			}
		};

		collectionInfoContainer.appendChild(collectionViewButton);
		collectionInfoContainer.appendChild(collectionStatus);

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
			document.getElementById('saveToChromaBtn').disabled = false;
			closePromptModal();
		};

		buttonContainer.appendChild(selectButton);

		modalBody.innerHTML = `
        <p><strong>Creation date:</strong> ${new Date(prompt.created_at).toLocaleString()}</p>
        <p><strong>Modification date:</strong> ${new Date(prompt.updated_at).toLocaleString()}</p>
        <p><strong>prompt content:</strong></p>
        <div class="prompt-content">${prompt.prompt_text}</div>
    `;

		// 모달 콘텐츠 업데이트
		const modalContent = promptModal.querySelector('.prompt-modal-content');
		const existingBody = modalContent.querySelector('.prompt-modal-body');
		if (existingBody) {
			existingBody.remove();
		}

		// 기존 collection info container 제거
		const existingCollectionInfo = modalContent.querySelector('.collection-info-container');
		if (existingCollectionInfo) {
			existingCollectionInfo.remove();
		}

		// 기존 button container 제거
		const existingButtonContainer = modalContent.querySelector('.prompt-button-container');
		if (existingButtonContainer) {
			existingButtonContainer.remove();
		}

		modalContent.appendChild(collectionInfoContainer);
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



/* ///////////////////////////////////// 쇼츠 생성 관련 js /////////////////////////////////// */

// Shorts 생성 관련 코드
document.addEventListener('DOMContentLoaded', () => {
	const collectionNameForm = document.getElementById('shortsGenerationForm');
	const searchTextForm = document.getElementById('shortsSearchForm');
	const videoNameForm = document.getElementById('shortsVideoNameForm');
	const createShortsBtn = document.getElementById('createShortsBtn');
	const buttonContainer = document.getElementById('shortsButtonContainer');

	// 폼 입력 감지하여 버튼 활성화
	function checkForms() {
		const collectionName = collectionNameForm.querySelector('textarea').value.trim();
		const searchText = searchTextForm.querySelector('textarea').value.trim();
		const videoName = videoNameForm.querySelector('textarea').value.trim();
		createShortsBtn.disabled = !(collectionName && searchText && videoName);
	}

	collectionNameForm.querySelector('textarea').addEventListener('input', checkForms);
	searchTextForm.querySelector('textarea').addEventListener('input', checkForms);
	videoNameForm.querySelector('textarea').addEventListener('input', checkForms);

	// 쇼츠 생성 버튼 클릭 이벤트
	createShortsBtn.addEventListener('click', async () => {
		const collectionName = collectionNameForm.querySelector('textarea').value.trim();
		const searchText = searchTextForm.querySelector('textarea').value.trim();
		const videoName = videoNameForm.querySelector('textarea').value.trim();

		// 로딩 UI 추가
		buttonContainer.innerHTML = `
            <div id="shorts-loading-spinner">
                <img src="/static/frontEnd/createShorts/gif/duck.gif" alt="Loading..." width="150">
                <p class="processing-text">Processing...</p>
            </div>
        `;

		try {
			// 첫 번째 API 호출
			const searchResponse = await fetch('http://127.0.0.1:5000/chroma/search', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					collectionName: collectionName,
					searchText: searchText
				})
			});

			if (!searchResponse.ok) {
				throw new Error('Search failed');
			}

			const searchData = await searchResponse.json();
			searchData.createVideoName = videoName;

			// 두 번째 API 호출
			const mergeResponse = await fetch('http://127.0.0.1:5000/video/merge', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(searchData )
			});

			if (!mergeResponse.ok) {
				throw new Error('Video merge failed');
			}

			// 성공 UI로 변경
			buttonContainer.innerHTML = `
                <div class="shorts-success-message">
                    <p>Shorts video created successfully!</p>
                </div>
                <button id="createShortsBtn" class="shorts-create-button">
                    Create shorts video
                </button>
            `;

		} catch (error) {
			console.error('Error:', error);
			buttonContainer.innerHTML = `
                <div class="shorts-error-message">
                    <p>Failed to create shorts video. Please try again.</p>
                </div>
                <button id="createShortsBtn" class="shorts-create-button">
                    Create shorts video
                </button>
            `;
		}
	});
});