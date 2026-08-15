import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import cyberwatchLogo from "../assets/cyberwatchlogo-rm.png";

function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleLogin = async (event) => {

        event.preventDefault();

        setErrorMessage("");
        setIsLoading(true);

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/api/v1/auth/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );

            const data = await response.json();

            console.log("Login Response:", data);

            if (!response.ok) {

                setErrorMessage(data.message);
                setIsLoading(false);
                return;

            }

            localStorage.setItem("token", data.token);

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            navigate("/dashboard");

        } catch (error) {

            console.error(error);

            setErrorMessage(
                "Unable to connect to the server."
            );

        } finally {

            setIsLoading(false);

        }

    };

    return (

        <div className="login-page">

            <div className="branding-section">

                <img
                    src={cyberwatchLogo}
                    alt="CyberWatch Logo"
                    className="branding-logo"
                />

            </div>

            <div className="login-card">

                <h2 className="login-title">
                    Welcome Back
                </h2>

                <p className="login-subtitle">
                    Sign in to continue to CyberWatch
                </p>

                {errorMessage && (
                    <div className="login-error">
                        {errorMessage}
                    </div>
                )}

                <form onSubmit={handleLogin}>

                    <div className="form-group">

                        <label>Username</label>

                        <input
                            type="text"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => {
                                setUsername(e.target.value);
                                setErrorMessage("");
                            }}
                        />

                    </div>

                    <div className="form-group">

                        <label>Password</label>

                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setErrorMessage("");
                            }}
                        />

                    </div>

                    <button
                        type="submit"
                        className="login-button"
                        disabled={isLoading}
                    >
                        {isLoading ? "Signing in..." : "Login"}
                    </button>

                </form>

            </div>

        </div>

    );

}

export default Login;