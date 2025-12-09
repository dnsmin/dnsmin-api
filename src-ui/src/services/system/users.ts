import {RefObject} from 'react';
import {GridDataSource, GridGetRowsParams, GridGetRowsResponse} from '@mui/x-data-grid';
import {GridApiPro} from '@mui/x-data-grid-pro';
import {IUser} from '@app/types/system/users';

type UsersCallback = (totalRecords: number, filteredRecords: number) => void;

export class UsersService {
    private subscribers: Set<UsersCallback> = new Set();
    private _gridApiRef: RefObject<GridApiPro> | null = null;
    private _gridDatasource: GridDataSource | null = null;
    private _records: IUser[] = [];
    private _totalRecords: number = 0;
    private _totalFilteredRecords: number = 0;

    private emit(totalRecords: number, filteredRecords: number) {
        this._totalRecords = totalRecords;
        this._totalFilteredRecords = filteredRecords;
        for (const cb of this.subscribers) cb(totalRecords, filteredRecords);
    }

    async getRecords(params: GridGetRowsParams): Promise<GridGetRowsResponse> {
        const response = await fetch('/api/v1/auth/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        });

        const data = await response.json();

        this._records = data.records;
        this.emit(data.total, data.records.length);

        return {
            rows: data.records,
            rowCount: data.total,
        };
    }

    async saveRecord(record: IUser) {
        // TODO
        console.warn('TODO: Save user to server!');
        this._gridApiRef?.current?.dataSource.cache.clear();
        await this._gridApiRef?.current?.dataSource.fetchRows();
    }

    get gridProps(): object {
        return {
            dataSource: this.gridDatasource,
            onStateChange: this.gridStateChangeHandler.bind(this),
            onDataSourceError: this.gridDataSourceErrorHandler.bind(this),
        }
    }

    get gridDatasource(): GridDataSource {
        if (this._gridDatasource !== null) {
            return this._gridDatasource;
        }

        this._gridDatasource = {
            getRows: this.getRecords.bind(this),
        };

        return this._gridDatasource;
    }

    get gridApiRef(): RefObject<GridApiPro> | null {
        return this._gridApiRef;
    }

    set gridApiRef(value: RefObject<GridApiPro>) {
        this._gridApiRef = value;
    }

    get records(): IUser[] {
        return this._records;
    }

    get totalRecords(): number {
        return this._totalRecords;
    }

    get totalFilteredRecords(): number {
        return this._totalFilteredRecords;
    }

    gridStateChangeHandler() {
        const totalRows = this._gridApiRef?.current?.getRowsCount();
        this.emit(this._totalRecords, totalRows || this._totalFilteredRecords);
    }

    gridDataSourceErrorHandler(): (error: any) => void {
        return (error: any) => {
            console.error('Grid Datasource Error:', error);
            // TODO
        }
    }

    onUsersStateChanged(callback: UsersCallback): () => void {
        this.subscribers.add(callback);

        callback(this._totalRecords, this._totalFilteredRecords);

        return () => {
            this.subscribers.delete(callback);
        };
    }
}

export const usersService = new UsersService();
