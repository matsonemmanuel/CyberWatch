import { useState } from "react";
import "../styles/login.css";
import cyberwatchLogo from "../assets/cyberwatch-logo.png";

function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (event) => {

        event.preventDefault();

        try {

    const response = await fetch(
        "http://127.0.0.1:5000/api/v1/auth/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })
        }
    );

    const data = await response.json();

    console.log(data);

} catch (error) {

    console.error(error);

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

                <p className="branding-tagline">
                    - Monitor. Detect. Protect -
                </p>
            </div>

            <div className="login-card">

                <h2 className="login-title">
                    Welcome Back
                </h2>

                <p className="login-subtitle">
                    Sign in to continue to CyberWatch
                </p>

                <form onSubmit={handleLogin}>

                    <div className="form-group">
                        <label>Username</label>

                        <input
                            type="text"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>

                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        className="login-button"
                    >
                        Login
                    </button>

                </form>

            </div>

        </div>
    );
}

export default Login;