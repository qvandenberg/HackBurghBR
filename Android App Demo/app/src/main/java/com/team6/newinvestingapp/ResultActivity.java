package com.team6.newinvestingapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ResultActivity extends AppCompatActivity {

    List<Double> low;
//    TextView txtResult;

    static final String TAG = "Hello";
    static Retrofit retrofit = null;
    static final String BASE_URL = "http://10.0.2.2:5000";


    static String SAVING_MESSAGE = "saving_message";
    static String INCOME_MESSAGE = "income_message";
    static String INVEST_MESSAGE = "invest_message";
    static String TIMEFRAME_MESSAGE = "timeframe_message";


    String ptSavings;
    String ptIncome;
    String ptInvest;
    String spinnerTimeFrame;

//    float saving;
//    float income;
//    float time;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        Intent intent = getIntent();

        ptSavings = intent.getStringExtra(SAVING_MESSAGE).toLowerCase();
        ptIncome = intent.getStringExtra(INCOME_MESSAGE).toLowerCase();
        ptInvest = intent.getStringExtra(INVEST_MESSAGE).toLowerCase();
        spinnerTimeFrame = intent.getStringExtra(TIMEFRAME_MESSAGE).toLowerCase();

//        saving = Float.parseFloat(ptSavings);
//        income = Float.parseFloat(ptIncome);
//        time = Float.parseFloat(spinnerTimeFrame);


        System.out.println("ptSaving " + ptSavings);
        System.out.println("ptIncome " + ptIncome);

//        txtResult = (TextView) findViewById(R.id.txtResult);
        connect();
//        txtResult = (TextView) findViewById(R.id.txtResult);

    }

    private void connect() {
        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }

        APIService apiService = retrofit.create(APIService.class);

        Call<Model> call = apiService.getData(spinnerTimeFrame, ptSavings, ptIncome);

        call.enqueue(new Callback<Model>() {

            @Override
            public void onResponse(Call<Model> call, Response<Model> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i(TAG, "Response");

                    for (int i = 0; i < low.size(); i++) {
                        System.out.println(low.get(i));
                    }

                }
            }

            @Override
            public void onFailure(Call<Model> call, Throwable t) {
                Log.i(TAG, "onFailure $t");
                Log.i("FAILURE", "I coudln't connect");
            }
        });

    }

}