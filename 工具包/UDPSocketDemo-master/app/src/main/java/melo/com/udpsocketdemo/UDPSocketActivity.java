package melo.com.udpsocketdemo;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;


import melo.com.udpsocketdemo.socket.UDPSocket;

import static java.lang.Math.abs;

/**
 * Created by melo on 2017/9/20.
 */

public class UDPSocketActivity extends AppCompatActivity {

    private double lastReceiveTime = 0;
    private String location ;
    private static final long TIME_OUT = 60 * 1000;
    private static final double HEARTBEAT_MESSAGE_DURATION = 1 * 1000;
    private static final String TAG = "UDPSocket";
    private UDPSocket socket;
    private double Time = 0;
    private double endTime = 0;
    private double duration = 0;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_socket);
        final EditText etMessage = (EditText) findViewById(R.id.et_message);
        Button btSend = (Button) findViewById(R.id.bt_send);
        socket = new UDPSocket(this);
        socket.startUDPSocket();

        //location = etMessage.getText().toString();
        btSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                location = etMessage.getText().toString();
                socket.sendMessage(etMessage.getText().toString());
                Time = System.currentTimeMillis();
                while(true){
                    endTime = System.currentTimeMillis();
                    socket.sendMessage(location);
                    crazySend();
                    Log.d(TAG, "duration:" + (endTime - Time));
                    if((endTime - Time) > TIME_OUT)
                        break;
//                double duration = System.currentTimeMillis() - lastReceiveTime;
//                Log.d(TAG, "duration:" + duration);
//                if (duration > TIME_OUT) {//若超过两分钟都没收到我的心跳包，则认为对方不在线。
//                    Log.d(TAG, "超时，对方已经下线");
//                    // 刷新时间，重新进入下一个心跳周期
//                    lastReceiveTime = System.currentTimeMillis();
//                } else if (duration > HEARTBEAT_MESSAGE_DURATION) {//若超过十秒他没收到我的心跳包，则重新发一个。不发心跳包
//                    socket.sendMessage(location);
//                }
                }
            location = "default";
            }
        });
    }


    @Override
    protected void onDestroy() {
        super.onDestroy();
        socket.stopUDPSocket();
    }

    protected void crazySend(){
        lastReceiveTime = System.currentTimeMillis();
        String string = "Crazy seding UDP package";
        while(true){
        Thread.currentThread();
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace(); }
        socket.sendMessage(string);
            Log.d(TAG, "duration:" + (lastReceiveTime - System.currentTimeMillis()));
        if (abs(lastReceiveTime - System.currentTimeMillis()) > 1000)break;
    }
    }
}
