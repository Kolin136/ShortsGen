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



// 비디오 분리 요청후 폴링 방식인 30초 단위로 완료했나 확인
document.addEventListener('DOMContentLoaded', () => {
	const videoFileInput = document.getElementById('videoFile');
	const uploadButton = document.getElementById('uploadButton');
	const uploadContainer = document.querySelector('.card'); // 업로드 영역
	const inputContainer = document.querySelector('.input-container');
	const progressText = document.getElementById('progressText');

	videoFileInput.addEventListener('change', () => {
		if (videoFileInput.files.length > 0) {
			uploadButton.disabled = false;
		}
	});

	uploadButton.addEventListener('click', async () => {
		if (videoFileInput.files.length === 0) return;

		const file = videoFileInput.files[0];
		console.log('Uploading:', file.name);

		uploadButton.disabled = true;
		inputContainer.style.display = 'none'; // 파일 선택 숨김
		uploadButton.style.display = 'none'; // 업로드 버튼 숨김

		// 🛠️ 로딩 UI 추가
		uploadContainer.innerHTML += `
    <div id="loading-spinner">
        <img src="/static/frontEnd/index/gif/duck.gif" alt="Loading..." width="150">
        <p class="processing-text">Processing...</p>
    </div>
		`;

		const formData = new FormData();
		formData.append('video', file);

		try {
			const response = await fetch('http://127.0.0.1:5000/video/split', {
				method: 'POST',
				body: formData,
			});

			if (response.ok) {
				const data = await response.json();
				const taskId = data.task_id;
				console.log(`Task ID: ${taskId}`);

				await pollTaskStatus(taskId);
			} else {
				console.error('Upload failed:', await response.text());
				alert('Upload failed. Please try again.');
			}
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred. Please try again.');
		}
	});
});

// 30초 단위 폴링
async function pollTaskStatus(taskId) {
	const pollingUrl = `http://127.0.0.1:5000/video/split/task-status/${taskId}`;
	let polling = true;

	while (polling) {
		try {
			const response = await fetch(pollingUrl);
			if (response.ok) {
				const statusData = await response.json();
				console.log('Polling response:', statusData);

				if (statusData.state === 'PENDING') {
					console.log('Task is still pending. Retrying in 30 seconds...');
					await wait(30000);
				} else if (statusData.state === 'SUCCESS') {
					console.log('Task completed successfully:', statusData);

					// 🎉 로딩 UI 제거 후 성공 메시지 표시
					document.getElementById('loading-spinner').innerHTML = `
							<p class="success-text">✅ Video Split Successful!</p>
					`;

					polling = false;
				} else {
					console.error('Unexpected task state:', statusData.state);
					alert(`Task failed with state: ${statusData.state}`);
					polling = false;
				}
			} else {
				console.error('Failed to fetch task status:', await response.text());
				alert('Failed to fetch task status. Stopping polling.');
				polling = false;
			}
		} catch (error) {
			console.error('Error during polling:', error);
			alert('An error occurred during polling. Stopping.');
			polling = false;
		}
	}
}

function wait(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

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


//  프롬프트 생성
document.addEventListener('DOMContentLoaded', () => {
	const promptForm = document.getElementById('promptForm');

	promptForm.addEventListener('submit', async (e) => {
		e.preventDefault();

		const promptText = promptForm.querySelector('textarea[name="prompt"]').value;

		try {
			const response = await fetch('http://127.0.0.1:5000/prompt/save', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					prompt: promptText
				})
			});

			if (response.ok) {
				alert('Prompt saved successfully!');
				promptForm.reset();
			} else {
				alert('Failed to save prompt. Please try again.');
			}
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred while saving the prompt.');
		}
	});
});



// 프롬프트 목록 로딩
document.addEventListener('DOMContentLoaded', async () => {
	const promptListContainer = document.getElementById('promptListContainer');
	const modal = document.getElementById('promptModal');
	const closeButton = document.querySelector('.close-button');
	let isEditMode = false;

	// Modal 닫기 함수
	const closeModal = () => {
		if (isEditMode) {
			if (confirm('There are unsaved changes. Are you sure you want to close?')) {
				isEditMode = false;
				modal.classList.remove('show-modal');
				setTimeout(() => {
					modal.style.display = 'none';
				}, 250);
			}
		} else {
			modal.classList.remove('show-modal');
			setTimeout(() => {
				modal.style.display = 'none';
			}, 250);
		}
	};

	// Modal 열기 함수
	const openModal = (prompt) => {
		isEditMode = false;
		document.getElementById('modalTitle').textContent = prompt.title;

		const modalBody = document.createElement('div');
		modalBody.className = 'modal-body';

		// 버튼 컨테이너 생성
		const buttonContainer = document.createElement('div');
		buttonContainer.className = 'modal-button-container';

		// 수정 버튼 생성
		const editButton = document.createElement('button');
		editButton.textContent = 'update';
		editButton.className = 'modal-edit-button';

		// 삭제 버튼 생성
		const deleteButton = document.createElement('button');
		deleteButton.textContent = 'delete';
		deleteButton.className = 'modal-delete-button';

		// 수정 버튼 클릭 이벤트
		editButton.onclick = () => {
			isEditMode = true;
			const promptContent = modalBody.querySelector('.prompt-content');
			const originalText = promptContent.textContent;

			const editContainer = document.createElement('div');
			editContainer.className = 'edit-container';

			editContainer.innerHTML = `
                <textarea class="modal-edit-textarea">${originalText}</textarea>
                <div class="modal-edit-buttons">
                    <button id="saveButton" class="modal-save-button">save</button>
                    <button id="cancelButton" class="modal-cancel-button">cancle</button>
                </div>
            `;

			promptContent.replaceWith(editContainer);

			editContainer.querySelector('#saveButton').onclick = () => savePrompt(prompt.prompt_id);
			editContainer.querySelector('#cancelButton').onclick = () => cancelEdit();
		};

		// 삭제 버튼 클릭 이벤트
		deleteButton.onclick = async () => {
			if (prompt.prompt_id && confirm('Are you sure you want to delete this prompt?')) {
				try {
					const response = await fetch(`http://127.0.0.1:5000/prompt/delete/${prompt.prompt_id}`, {
						method: 'DELETE'
					});
					if (response.ok) {
						alert('Prompt has been deleted successfully.');
						closeModal();
						location.reload();
					}
				} catch (error) {
					console.error('Delete error:', error);
					alert('An error occurred while deleting.');
				}
			}
		};

		buttonContainer.appendChild(editButton);
		buttonContainer.appendChild(deleteButton);

		modalBody.innerHTML = `
            <p><strong>Creation date:</strong> ${new Date(prompt.created_at).toLocaleString()}</p>
            <p><strong>Modification date:</strong> ${new Date(prompt.updated_at).toLocaleString()}</p>
            <p><strong>prompt content:</strong></p>
            <div class="prompt-content">${prompt.prompt_text}</div>
        `;

		const modalContent = modal.querySelector('.modal-content');
		const existingBody = modal.querySelector('.modal-body');
		if (existingBody) {
			existingBody.remove();
		}
		modalContent.appendChild(buttonContainer);
		modalContent.appendChild(modalBody);

		modal.style.display = 'block';
		setTimeout(() => {
			modal.classList.add('show-modal');
		}, 10);
	};

	// 취소 버튼용 전역 함수 추가
	window.cancelEdit = () => {
		if (confirm('Are you sure you want to cancel the changes?')) {
			isEditMode = false;
			location.reload(); // 또는 원래 상태로 되돌리는 로직 구현
		}
	};

	// 저장 함수 수정
	window.savePrompt = async (promptId) => {
		const textarea = modal.querySelector('textarea');
		const updatedText = textarea.value;

		try {
			const response = await fetch('http://127.0.0.1:5000/prompt/update', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					promptId: promptId,
					updatePrompt: updatedText
				})
			});

			if (response.ok) {
				isEditMode = false; // 저장 성공시 수정 모드 해제
				alert('Prompt has been updated successfully.');
				location.reload();
			}
		} catch (error) {
			console.error('Update error:', error);
			alert('An error occurred while updating.');
		}
	};

	// 닫기 버튼 이벤트
	closeButton.addEventListener('click', closeModal);

	// 모달 바깥 클릭시 닫기
	window.addEventListener('click', (e) => {
		if (e.target === modal) {
			closeModal();
		}
	});

	// ESC 키로 모달 닫기
	document.addEventListener('keydown', (e) => {
		if (e.key === 'Escape' && modal.style.display === 'block') {
			closeModal();
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
			article.className = 'item';
			article.style.width = 'calc(25% - 15px)';
			article.style.marginBottom = '20px';
			article.style.cursor = 'pointer';

			article.innerHTML = `
        <header>
          <h3>${prompt.title}</h3>
        </header>
      `;

			article.addEventListener('click', () => {
				openModal(prompt);
			});

			flexContainer.appendChild(article);
		});

		colDiv.appendChild(flexContainer);
		promptListContainer.appendChild(colDiv);

	} catch (error) {
		console.error('Failed to load prompt list:', error);
	}
});
