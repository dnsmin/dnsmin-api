import * as React from "react";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {Button, Grid} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import {
    DataGridPro,
    GridFilterModel,
    GridSortModel,
    GridPaginationModel,
    GridLogicOperator,
    GridColDef,
    GridActionsCellItem,
} from "@mui/x-data-grid-pro";
import {useAZones} from "@app/features/zones/azones/hooks";
import PageHeader from "@components/PageHeader";
import StatisticCard from "@components/cards/StatisticCard";


interface ViewProps {
    basePath: string;
}

const ListView = ({basePath}: ViewProps) => {
    const navigate = useNavigate();

    const [filterModel, setFilterModel] = useState<GridFilterModel>({
        items: [],
        quickFilterValues: [],
        logicOperator: GridLogicOperator.And,
    });

    const [sortModel, setSortModel] = useState<GridSortModel>([]);

    const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({page: 0, pageSize: 5});

    const {data, isLoading} = useAZones({filterModel, sortModel, paginationModel});

    const isFilteringActive = React.useMemo(() => {
        return filterModel.items.length > 0 || (filterModel.quickFilterValues?.length ?? 0) > 0;
    }, [filterModel]);

    const openCreate = () => {
        navigate(`${basePath}/create`);
    };

    const openUpdate = (id: string) => {
        navigate(`${basePath}/${id}/update`);
    };

    const openDelete = (id: string) => {
        navigate(`${basePath}/${id}/delete`);
    };

    const columns: readonly GridColDef<any>[] = [
        {field: 'id', headerName: 'Zone ID', width: 150},
        {field: 'tenantId', headerName: 'Tenant ID', width: 150},
        {field: 'viewId', headerName: 'View ID', width: 150},
        {field: 'fqdn', headerName: 'FQDN', width: 200},
        {field: 'kind', headerName: 'Type', width: 200},
        {field: 'serial', headerName: 'Serial', width: 150},
        {field: 'dnssec', headerName: 'DNSSEC', width: 150},
        {field: 'catalog', headerName: 'Catalog', width: 150},
        {field: 'shared', headerName: 'Shared', width: 150},
        {field: 'createdAt', headerName: 'Created', width: 175},
        {field: 'updatedAt', headerName: 'Updated', width: 175},
        {
            field: 'actions',
            type: 'actions',
            headerName: 'Actions',
            width: 100,
            getActions: (params) => [
                <GridActionsCellItem
                    key="edit"
                    icon={<EditIcon/>}
                    label="Edit"
                    onClick={() => openUpdate(params.row.id)}
                    showInMenu
                />,
                <GridActionsCellItem
                    key="delete"
                    icon={<DeleteIcon/>}
                    label="Delete"
                    onClick={() => openDelete(params.row.id)}
                    showInMenu
                />,
            ],
        },
    ];

    return (
        <>
            <PageHeader title={'Authoritative Zones'}/>
            <Grid container justifyContent="space-between">
                <Grid size={{sm: 12, md: 6, lg: 4}} paddingY={2}>
                    <Grid container spacing={2}>
                        <Grid size={{sm: 12, md: 6}}>
                            <StatisticCard label="Total Zones" value={data?.total}/>
                        </Grid>
                        {isFilteringActive && (
                            <Grid size={{sm: 12, md: 6}}>
                                <StatisticCard label="Total Results" value={data?.totalFiltered}/>
                            </Grid>
                        )}
                    </Grid>
                </Grid>
                <Grid size={{sm: 12, md: 3, lg: 2}} paddingY={2} display="flex" justifyContent="flex-end"
                      alignItems="flex-end">
                    <Button variant="contained" onClick={() => openCreate()}>Create Zone</Button>
                </Grid>
                <Grid size={12}>
                    <DataGridPro
                        autoHeight
                        loading={isLoading}
                        columns={columns}
                        rows={data?.records ?? []}
                        getRowId={(row) => row.id}
                        rowCount={data?.totalFiltered ?? 0}
                        filterMode="server"
                        sortingMode="server"
                        paginationMode="server"
                        pagination={true}
                        pageSizeOptions={[5, 10, 25, 50, 100]}
                        filterModel={filterModel}
                        sortModel={sortModel}
                        paginationModel={paginationModel}
                        onFilterModelChange={(model) => setFilterModel(model)}
                        onSortModelChange={(model) => setSortModel(model)}
                        onPaginationModelChange={(model) => setPaginationModel(model)}
                        initialState={{
                            pinnedColumns: {
                                right: ['actions'],
                            },
                        }}
                    />
                </Grid>
            </Grid>
        </>
    );
};

export default ListView;
