"use client";

import {FallbackProps} from 'react-error-boundary'

export default function ErrorPage({error, resetErrorBoundary}: FallbackProps) {
    // DEV mode response
    if (import.meta.env.DEV)
        return (
            <div role="alert" style={{padding: "2em"}}>
                <h1>React Error Occurred!</h1>
                <p>Error Details:</p>
                <pre style={{color: "red"}}>{error.message}</pre>
            </div>
        );

    // All other modes response
    return (
        <div role="alert" style={{padding: "2em"}}>
            <h1>Error Occurred!</h1>
            <p>Please contact a system administrator about your issue.</p>
        </div>
    );
}
