import {http} from "@app/api/http";
import {UserInDTO, UsersPagedResponseDTO} from "@app/types/dto/auth";
import {User, UsersPaged} from "@app/types/models/auth";
import {userFromDTO, userToDTO, usersPagedFromDTO} from "@app/api/converters/auth";
import {ListResourceParams} from "@app/services/base";

export const UserService = {
    async list(req?: ListResourceParams): Promise<UsersPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<UsersPagedResponseDTO>(
            "/auth/users", params
        );

        return usersPagedFromDTO(response.data);
    },

    async get(id: string): Promise<User> {
        const response = await http.get<UserInDTO>(`/auth/users/${id}`);
        return userFromDTO(response.data);
    },

    async create(payload: Omit<User, "id">): Promise<User> {
        const dtoPayload = userToDTO(payload as User);
        const response = await http.post<UserInDTO>("/auth/users/create", dtoPayload);
        return userFromDTO(response.data);
    },

    async update(id: string, payload: Partial<User>): Promise<User> {
        const dtoPayload = userToDTO(payload as User);
        const response = await http.put<UserInDTO>(`/auth/users/${id}`, dtoPayload);
        return userFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/auth/users/${id}`);
    },
};