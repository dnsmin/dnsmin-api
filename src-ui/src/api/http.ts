import axios from "axios";

export const http = axios.create({
    baseURL: '/api/v1',
    withCredentials: true,
});

http.interceptors.response.use(
    (res) => res,
    (err) => {
        console.error("API error:", err);
        return Promise.reject(err);
    }
);