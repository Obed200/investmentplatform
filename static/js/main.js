console.log('Ribural static files loaded.');

function setupReferralShare() {
	const copyBtn = document.getElementById('copyReferral');
	const shareBtn = document.getElementById('shareReferral');
	const waBtn = document.getElementById('waShare');
	const input = document.getElementById('referralLink');
	if (!input) return;
	const link = input.value;
	if (copyBtn) {
		copyBtn.addEventListener('click', () => {
			input.select();
			try {
				document.execCommand('copy');
				copyBtn.textContent = 'Copied';
				setTimeout(() => copyBtn.textContent = 'Copy', 2000);
			} catch (e) {
				alert('Copy failed. Please select and copy manually.');
			}
		});
	}
	if (shareBtn && navigator.share) {
		shareBtn.addEventListener('click', async () => {
			try {
				await navigator.share({ title: 'Join Ribural', text: 'Join Ribural Investments', url: link });
			} catch (err) {
				console.warn('Share failed', err);
			}
		});
	} else if (shareBtn) {
		shareBtn.style.display = 'none';
	}
	if (waBtn) {
		waBtn.href = `https://wa.me/?text=${encodeURIComponent(link)}`;
	}
}

document.addEventListener('DOMContentLoaded', setupReferralShare);

function setupPasswordToggles() {
	const pwdInputs = document.querySelectorAll('input[type="password"]');
	pwdInputs.forEach((input) => {
		if (input.dataset.pwtAttached) return;
		input.dataset.pwtAttached = '1';
		const btn = document.createElement('button');
		btn.type = 'button';
		btn.className = 'password-toggle';
		btn.setAttribute('aria-label', 'Toggle password visibility');
		btn.textContent = 'Show';
		btn.addEventListener('click', () => {
			if (input.type === 'password') {
				input.type = 'text';
				btn.textContent = 'Hide';
			} else {
				input.type = 'password';
				btn.textContent = 'Show';
			}
			input.focus();
		});
		// Insert after the input field
		input.insertAdjacentElement('afterend', btn);
	});
}

document.addEventListener('DOMContentLoaded', setupPasswordToggles);
