package com.team6.newinvestingapp;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Model {

    @SerializedName("low")
    @Expose
    private List<Double> low = null;
    @SerializedName("mid")
    @Expose
    private List<Double> mid = null;
    @SerializedName("savings_only")
    @Expose
    private List<Double> savingsOnly = null;
    @SerializedName("time")
    @Expose
    private List<Double> time = null;
    @SerializedName("up")
    @Expose
    private List<Double> up = null;

    public List<Double> getLow() {
        return low;
    }

    public List<Double> getMid() {
        return mid;
    }

    public List<Double> getSavingsOnly() {
        return savingsOnly;
    }

    public List<Double> getTime() {
        return time;
    }


    public List<Double> getUp() {
        return up;
    }

    public void setUp(List<Double> up) {
        this.up = up;
    }

}