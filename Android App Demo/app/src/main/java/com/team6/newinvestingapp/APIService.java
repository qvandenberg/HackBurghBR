package com.team6.newinvestingapp;

import retrofit2.http.GET;
import retrofit2.http.Query;

import retrofit2.Call;

public interface APIService {
    @GET("api/v1/prognosis")
    Call<Model> getData(@Query("time") String time, @Query("current_savings") String saving, @Query("monthly_savings") String income);

}