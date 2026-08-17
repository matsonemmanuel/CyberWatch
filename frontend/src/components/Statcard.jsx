import "../styles/statcard.css";

function StatCard({ icon, title, value }) {

    return (
        <div className="stat-card">

            <div className="stat-icon">
                {icon}
            </div>

            <div className="stat-content">

                <p className="stat-title">
                    {title}
                </p>

                <p className="stat-value">
                    {value}
                </p>

            </div>

        </div>
    );
}

export default StatCard;