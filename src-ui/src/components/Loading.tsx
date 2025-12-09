import {Container} from '@mui/material';
import Logo from '@app/assets/img/logo-icon.svg';
import * as React from "react";

export const Loading = () => {
    return (
        <Container sx={{display: 'flex', minHeight: '96vh', justifyContent: 'center', alignItems: 'center'}}>
            <img src={Logo} className="loadingLogo" alt="DNSMin Logo" height={150}/>
        </Container>
    );
};
