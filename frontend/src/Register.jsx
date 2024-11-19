import React from "react";
import { useState } from "react";
import axios from "axios";

export default function Registr() {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        phone_number: ""
    });

    const handleChange = (evt) => {
        const { name, value } = evt.target;
        setFormData({ ...formData, [name]: value  })
    }

    const handleSubmit = async (evt) => {
        evt.prevent.default();
        try{
            const response = await axios.post("http://localhost:6060/register", formData);
            alert("Registration successful!")
        } catch (error) {
            alert.apply(error.response?.data?.error || "Registration failed!")
        }
    };

    return(
        <form onSubmit={handleSubmit}>
            <input name="username" placeholder="Username" onChange={handleChange} required />
            <input name="email" type="email" placeholder="Email" onChange={handleChange} required />
            <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
            <input name="phone_number" placeholder="Phone Number" onChange={handleChange} required />
            <button type="submit">Register</button>
        </form>
    )
}
