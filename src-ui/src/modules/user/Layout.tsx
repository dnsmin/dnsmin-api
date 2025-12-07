import {Outlet} from 'react-router-dom';
import {Container, Stack} from '@mui/material';

import Header from '@modules/user/Header';
import Footer from '@modules/user/Footer';

export const Layout = () => {
    return (
        <>
            <Container maxWidth={false} disableGutters>
                <Stack>
                    <Header/>
                    <Container maxWidth={false} disableGutters sx={{paddingX: 1, mb: '30px'}}>
                        <Outlet/>
                    </Container>
                    <Footer/>
                </Stack>
            </Container>
        </>
    )
}

export default Layout
