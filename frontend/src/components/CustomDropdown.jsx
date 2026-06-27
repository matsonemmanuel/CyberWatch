import { useState } from "react";
import "../styles/customdropdown.css";

function CustomDropdown({
    options,
    selected,
    onSelect,
    fullWidth = false
}) {
    const [open, setOpen] = useState(false);

    return (

        <div
            className={`custom-dropdown ${fullWidth ? "full-width" : ""}`}
        >

            <button
                className="dropdown-button"
                onClick={() => setOpen(!open)}
            >

                <span>{selected}</span>

                <span className="dropdown-arrow">

                    {open ? "▲" : "▼"}

                </span>

            </button>

            {open && (

                <div className="dropdown-menu">

                    {options.map((option) => (

                        <div
                            key={option}
                            className="dropdown-item"
                            onClick={() => {

                                onSelect(option);

                                setOpen(false);

                            }}
                        >

                            {option}

                        </div>

                    ))}

                </div>

            )}

        </div>

    );

}

export default CustomDropdown;