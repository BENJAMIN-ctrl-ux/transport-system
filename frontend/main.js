
        // Form switching functionality
        const loginForm = document.getElementById('loginForm');
        const signupForm = document.getElementById('signupForm');
        const showSignupBtn = document.getElementById('showSignup');
        const showLoginBtn = document.getElementById('showLogin');

        showSignupBtn.addEventListener('click', () => {
            loginForm.classList.remove('active');
            signupForm.classList.add('active');
        });

        showLoginBtn.addEventListener('click', () => {
            signupForm.classList.remove('active');
            loginForm.classList.add('active');
        });

        // Form validation
        function validateEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        function validatePassword(password) {
            return password.length >= 6;
        }

        function showError(elementId, message) {
            const errorElement = document.getElementById(elementId);
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }

        function hideError(elementId) {
            const errorElement = document.getElementById(elementId);
            errorElement.style.display = 'none';
        }

        function showSuccess(message) {
            // Create and show success notification
            const successDiv = document.createElement('div');
            successDiv.className = 'success-message';
            successDiv.textContent = message;
            successDiv.style.display = 'block';
            successDiv.style.textAlign = 'center';
            successDiv.style.margin = '20px 0';
            successDiv.style.padding = '10px';
            successDiv.style.backgroundColor = '#d4edda';
            successDiv.style.border = '1px solid #c3e6cb';
            successDiv.style.borderRadius = '8px';
            
            const container = document.querySelector('.auth-container');
            container.appendChild(successDiv);
            
            setTimeout(() => {
                successDiv.remove();
            }, 3000);
        }

        // Login form submission
        document.getElementById('loginFormElement').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            // Clear previous errors
            hideError('loginEmailError');
            hideError('loginPasswordError');
            
            let isValid = true;
            
            if (!validateEmail(email)) {
                showError('loginEmailError', 'Please enter a valid email address');
                isValid = false;
            }
            
            if (!validatePassword(password)) {
                showError('loginPasswordError', 'Password must be at least 6 characters long');
                isValid = false;
            }
            
            if (isValid) {
                // Simulate login process
                const btn = e.target.querySelector('button');
                btn.textContent = 'Signing in...';
                btn.disabled = true;
                
                setTimeout(() => {
                    btn.textContent = 'Sign In';
                    btn.disabled = false;
                    showSuccess('Login successful! Welcome back.');
                    
                    // Here you would typically redirect to dashboard
                    console.log('Login successful:', { email, password });
                }, 1500);
            }
        });

        // Signup form submission
        document.getElementById('signupFormElement').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const userid = document.getElementById('signupUserid').value;
            const fullname = document.getElementById('signupFullname').value;
            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('signupConfirmPassword').value;
            const termsAccepted = document.getElementById('termsCheckbox').checked;
            
            // Clear previous errors
            hideError('signupUseridError');
            hideError('signupFullnameError');
            hideError('signupEmailError');
            hideError('signupPasswordError');
            hideError('signupConfirmPasswordError');
            
            let isValid = true;
            
            if (userid.length < 3) {
                showError('signupUseridError', 'User ID must be at least 3 characters long');
                isValid = false;
            }
            
            if (fullname.length < 2) {
                showError('signupFullnameError', 'Please enter your full name');
                isValid = false;
            }
            
            if (!validateEmail(email)) {
                showError('signupEmailError', 'Please enter a valid email address');
                isValid = false;
            }
            
            if (!validatePassword(password)) {
                showError('signupPasswordError', 'Password must be at least 6 characters long');
                isValid = false;
            }
            
            if (password !== confirmPassword) {
                showError('signupConfirmPasswordError', 'Passwords do not match');
                isValid = false;
            }
            
            if (!termsAccepted) {
                alert('Please accept the terms and conditions');
                isValid = false;
            }
            
            if (isValid) {
                // Simulate signup process
                const btn = e.target.querySelector('button');
                btn.textContent = 'Creating account...';
                btn.disabled = true;
                
                setTimeout(() => {
                    btn.textContent = 'Sign Up';
                    btn.disabled = false;
                    showSuccess('Account created successfully! Please check your email for verification.');
                    
                    // Clear form
                    e.target.reset();
                    
                    // Switch to login form
                    setTimeout(() => {
                        signupForm.classList.remove('active');
                        loginForm.classList.add('active');
                    }, 2000);
                    
                    console.log('Signup successful:', { userid, fullname, email });
                }, 2000);
            }
        });

        // Google sign-in
        document.getElementById('googleSignIn').addEventListener('click', () => {
            const btn = document.getElementById('googleSignIn');
            btn.textContent = 'Connecting to Google...';
            btn.disabled = true;
            
            setTimeout(() => {
                btn.textContent = 'Continue with Google';
                btn.disabled = false;
                showSuccess('Google sign-in would be implemented here');
            }, 1500);
        });

        // Forgot password
        document.getElementById('forgotPasswordLink').addEventListener('click', (e) => {
            e.preventDefault();
            const email = prompt('Please enter your email address:');
            if (email && validateEmail(email)) {
                showSuccess('Password reset link sent to your email');
            } else if (email) {
                alert('Please enter a valid email address');
            }
        });

        // Add input focus effects
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                input.parentElement.classList.remove('focused');
            });
        });