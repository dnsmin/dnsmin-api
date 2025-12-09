import * as React from "react";
import {Grid} from '@mui/material';
import i18n from '@app/utils/i18n';
import PageHeader from '@components/PageHeader';
import StatisticCard from '@components/cards/StatisticCard';

const Page = () => {
    return (
        <>
            <PageHeader title={i18n.t('pageTitles.dashboard')}/>
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
        </>
    );
};

export default Page;
