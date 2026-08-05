import React, { useState } from "react";
import "../styles/login_page.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { CircularProgress } from "react-cssfx-loading";
import CloseIcon from "@mui/icons-material/Close";

interface LoginPageProps {
    onClose?: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onClose }) => {

    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState("login");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleClose = () => {
        if (onClose) {
            onClose();
            return;
        }

        navigate("/home");
    };

    const [first_name, setfirst_name] = useState("");
    const [last_name, setlast_name] = useState("");
    const [email_id, setemail_id] = useState("");
    const [password, setpassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");


    //otp verify logic 
    const otp = async () => {

        const payload = {
            email_id: email_id
        };
        try {
            const response = await axios.post(
                "http://localhost:8000/otp",
                payload
            );

            if (response.data?.otp) {
                localStorage.setItem(
                    "dev_otp",
                    response.data.otp
                );
            }
        } catch (error) {
            console.warn("OTP Error:", error);
        }
    };

    // Login details validation function 
    const handleLogin = async () => {
        if (isSubmitting) return;

        const payload = {
            email_id: email_id,
            password: password
        };
        try {
            const response = await axios.post(
                "http://localhost:8000/login",
                payload
            );
            if (response.status === 200) {
                setIsSubmitting(true);
                localStorage.setItem("email_id", email_id);

                await otp();
                window.setTimeout(() => {
                    navigate("/otp_verify");
                }, 2000);

                return;
            }
        } catch (error: any) {
            setIsSubmitting(false);

            if (error.response?.status === 401) {

                setErrorMessage("Invalid Password");

            } else if (error.response?.status === 404) {

                setErrorMessage("User not found");

            } else {

                setErrorMessage("Server error. Please try again later.");
            }
        }
    };
    // Signup details validation function 
    const handleSignup = async () => {
        if (isSubmitting) return;

        const payload = {
            first_name: first_name,
            last_name: last_name,
            email_id: email_id,
            password: password
        };
        try {
            const response = await axios.post(
                "http://localhost:8000/signup",
                payload
            );

            if (response.status == 201) {
                alert("User already exists");
                return;
            }

            setIsSubmitting(true);
            alert("User registered successfully");
            localStorage.setItem("email_id", email_id);

            await otp();
            window.setTimeout(() => {
                navigate("/otp_verify");
            }, 2000);

        } catch (error: any) {
            setIsSubmitting(false);
            console.warn("Backend not available:", error);
        }
    };

    return (
        <div className="main-login-box">
            <div className="login-card">
                <div className="closeIcon" onClick={handleClose}>
                    <CloseIcon />
                </div>

                {/* Toggle Buttons */}
                <div className="switch-container">
                    <button
                        className={activeTab === "login" ? "active-tab" : ""}
                        onClick={() => setActiveTab("login")}
                    >
                        Login
                    </button>

                    <button
                        className={activeTab === "signup" ? "active-tab" : ""}
                        onClick={() => setActiveTab("signup")}
                    >
                        Signup
                    </button>
                </div>

                {/* LOGIN FORM */}
                {activeTab === "login" && (
                    <>
                        <div className="email-div">
                            <div className="email-text">Email Address</div>
                            <input
                                className="email-input"
                                type="email"
                                placeholder="Enter your email address"
                                value={email_id}
                                onChange={(e) => setemail_id(e.target.value)}
                            />
                        </div>

                        <div className="password-div">
                            <div className="password-text">
                                Enter Password
                            </div>
                            <input
                                className="password-input"
                                type="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setpassword(e.target.value)}
                            />
                        </div>

                        <div className="remember-me-forgot-password-div">
                            <div className="remember-me-div">
                                <input
                                    className="remember-me-checkbox"
                                    type="checkbox"
                                />
                                <label>Remember me</label>
                            </div>

                            <div className="forgot-password-div">
                                <label>Forgot Password?</label>
                            </div>
                        </div>

                        <div className="login-button-div">
                            <button className="login-button" onClick={handleLogin} disabled={isSubmitting}>
                                {isSubmitting ? (
                                    <span className="button-loader">
                                        <CircularProgress />
                                    </span>
                                ) : (
                                    "Login"
                                )}
                            </button>
                        </div>

                        <div className="sign-up-div">
                            <p>
                                Don't have an account?{" "}
                                <b
                                    style={{ cursor: "pointer" }}
                                    onClick={() => setActiveTab("signup")}
                                >
                                    Sign up
                                </b>
                            </p>
                        </div>
                    </>
                )}

                {/* SIGNUP FORM */}
                {activeTab === "signup" && (
                    <>
                        <div className="firstName-div">
                            <div className="firstName-text">
                                Enter Your First Name
                            </div>
                            <input
                                className="firstName-input"
                                type="text"
                                placeholder="Enter your first name"
                                value={first_name}
                                onChange={(e) =>
                                    setfirst_name(e.target.value)
                                }
                            />
                        </div>

                        <div className="lastName-div">
                            <div className="lastName-text">
                                Enter Your Last Name
                            </div>
                            <input
                                className="lastName-input"
                                type="text"
                                placeholder="Enter your last name"
                                value={last_name}
                                onChange={(e) =>
                                    setlast_name(e.target.value)
                                }
                            />
                        </div>

                        <div className="email-div">
                            <div className="email-text">
                                Enter Your Email Address
                            </div>
                            <input
                                className="email-input"
                                type="email"
                                placeholder="Enter your email address or phone number"
                                value={email_id}
                                onChange={(e) =>
                                    setemail_id(e.target.value)
                                }
                            />
                        </div>
                        <div className="password-div">
                            <div className="password-text">
                                Enter Password
                            </div>
                            <input
                                className="password-input"
                                type="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) =>
                                    setpassword(e.target.value)
                                }
                            />
                        </div>

                        <div className="confirmPassword-div">
                            <div className="password-text">
                                Confirm Password
                            </div>

                            <input
                                className="confirmPassword-input"
                                type="password"
                                placeholder="Confirm your password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />

                            {confirmPassword &&
                                password !== confirmPassword && (
                                    <div className="password-mismatch">
                                        Passwords do not match
                                    </div>
                                )}
                        </div>

                        <div className="signup-created">
                            <button className="account-created-button" onClick={handleSignup} disabled={isSubmitting}>
                                {isSubmitting ? (
                                    <span className="button-loader">
                                        <CircularProgress />
                                    </span>
                                ) : (
                                    "Sign Up"
                                )}
                            </button>
                        </div>

                        <div className="already-have-account">
                            <p>
                                Already have an account?{" "}
                                <b
                                    style={{ cursor: "pointer" }}
                                    onClick={() => setActiveTab("login")}
                                >
                                    Log-In Or
                                </b>
                            </p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default LoginPage;