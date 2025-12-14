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
import {useAuthClients} from "@app/features/auth/clients/hooks";
import PageHeader from "@components/PageHeader";
import StatisticCard from "@components/cards/StatisticCard";
import FormDialog from "@app/features/auth/clients/components/FormDialog";
import DeleteDialog from "@app/features/auth/clients/components/DeleteDialog";


interface ViewProps {
    basePath: string;
    multiTenant?: boolean;
}

const ListView = ({basePath, multiTenant = true}: ViewProps) => {
    const navigate = useNavigate();

    const [filterModel, setFilterModel] = useState<GridFilterModel>({
        items: [],
        quickFilterValues: [],
        logicOperator: GridLogicOperator.And,
    });

    const [sortModel, setSortModel] = useState<GridSortModel>([]);

    const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({page: 0, pageSize: 5});

    const {data, isLoading} = useAuthClients({filterModel, sortModel, paginationModel});

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
        {field: 'id', headerName: 'Client ID', width: 150},
        ...(multiTenant ? [{field: 'tenantId', headerName: 'Tenant ID', width: 150}] : []),
        {field: 'userId', headerName: 'User ID', width: 150},
        {field: 'name', headerName: 'Name', width: 300},
        {field: 'scopes', headerName: 'Scopes', width: 300},
        {field: 'enabled', headerName: 'Enabled', width: 100},
        {field: 'createdAt', headerName: 'Created', width: 175},
        {field: 'updatedAt', headerName: 'Updated', width: 175},
        {field: 'expiresAt', headerName: 'Expires', width: 175},
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
            <PageHeader title={'API Clients'}/>
            <Grid container justifyContent="space-between">
                <Grid size={{sm: 12, md: 6, lg: 4}} paddingY={2}>
                    <Grid container spacing={2}>
                        <Grid size={{sm: 12, md: 6}}>
                            <StatisticCard label="Total API Clients" value={data?.total}/>
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
                    <Button variant="contained" onClick={() => openCreate()}>Create API Client</Button>
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
            <FormDialog basePath={basePath}/>
            <DeleteDialog basePath={basePath}/>
        </>
    );
};

export default ListView;
