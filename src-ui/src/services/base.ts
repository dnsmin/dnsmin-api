import {GridFilterModel, GridPaginationModel, GridSortModel} from "@mui/x-data-grid-pro";

export interface ListResourceParams {
    filterModel: GridFilterModel;
    sortModel: GridSortModel;
    paginationModel: GridPaginationModel;
}
