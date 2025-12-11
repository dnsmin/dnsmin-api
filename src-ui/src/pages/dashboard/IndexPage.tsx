import * as React from "react";
import {Container, Grid} from '@mui/material';
import PageHeader from '@components/PageHeader';
import StatisticCard from '@components/cards/StatisticCard';

interface ViewProps {
    basePath: string;
}

const Page: React.FC<ViewProps> = () => {
    return (
        <>
            <Container maxWidth={false} sx={{marginY: 2}}>
                <PageHeader title={'Dashboard'}/>
                <Grid container spacing={2}>
                    <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                        <StatisticCard label="Total Users" value={0}/>
                    </Grid>
                    <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                        <StatisticCard label="Total Servers" value={0}/>
                    </Grid>
                    <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                        <StatisticCard label="Total Zones" value={0}/>
                    </Grid>
                    <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                        <StatisticCard label="Active User Sessions" value={0}/>
                    </Grid>
                </Grid>
            </Container>
        </>
    );
};

export default Page;
