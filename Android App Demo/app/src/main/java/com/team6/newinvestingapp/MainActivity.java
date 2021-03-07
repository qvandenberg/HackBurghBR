package com.team6.newinvestingapp;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.EditText;
import android.widget.Spinner;

import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    EditText ptSaving;
    EditText ptIncome;
    EditText ptInvest;
    Spinner spinnerTimeFrame;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);


        // remove bar
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getSupportActionBar().hide();

        setContentView(R.layout.activity_main);
    }


    public void onClickSubmit(View view) {
        Intent intent = new Intent(this, ResultActivity.class);

        ptSaving = (EditText) findViewById(R.id.ptSavings);
        ptIncome = (EditText) findViewById(R.id.ptIncome);
        ptInvest = (EditText) findViewById(R.id.ptInvest);
        spinnerTimeFrame = (Spinner) findViewById(R.id.spinnerTimeFrame);


        String saving = ptSaving.getText().toString();
        String income = ptIncome.getText().toString();
        String invest = ptInvest.getText().toString();
        String timeFrame = String.valueOf(spinnerTimeFrame.getSelectedItem());

        if (saving.equals("") || income.equals("") || invest.equals("")){
            return;
        }

        intent.putExtra(ResultActivity.SAVING_MESSAGE, saving);
        intent.putExtra(ResultActivity.INCOME_MESSAGE, income);
        intent.putExtra(ResultActivity.INVEST_MESSAGE, invest);
        intent.putExtra(ResultActivity.TIMEFRAME_MESSAGE, timeFrame);

        startActivity(intent);
    }




}