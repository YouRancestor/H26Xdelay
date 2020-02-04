# H264编码的编解码器延迟调研

## 结论

H264编码允许在编解码过程中零延迟，但与编解码器（主要是编码器）实现有关，需要编码器支持设置相关参数，不同编码器参数不一样。

## 测试与结果

### 测试内容

生成图像序列并在图像中央绘制图像序号，交由H264编码器进行编码，编码后的内容立即交给解码器解码。记录编解码器第一次返回非空前，返回为空的次数（即延迟帧数）。

### 测试结果

| 编码器 | 编码参数 | 编码延迟 | 解码延迟 |
| - | - | -: | -: |
| libx264 | default | 41 | 2 |
| libx264 | {'tune':'zerolatency'} | **0** | 0 |
| h264_nvenc | default | 2 | 0 |
| h264_nvenc | {'zerolatency':'1'} | 2 | 0 |
| h264_nvenc | {'delay':'0'} | **0** | 0 |
| libx265 | default | 30 | 2 |
| libx265 | {'tune':'zero-latency'} | 4 | 0 |

### 补充说明

- zerolatency （意为零延迟）是一组预设策略，也可通过分别指定编码器的相关参数来达到同样效果。参考x264_param_apply_tune。使用该策略会导致码流增大10%左右。

```c
        // ...
        else if( !strncasecmp( s, "zerolatency", 11 ) )
        {
            param->rc.i_lookahead = 0;
            param->i_sync_lookahead = 0;
            param->i_bframe = 0; // 关闭b帧
            param->b_sliced_threads = 1;
            param->b_vfr_input = 0;
            param->rc.b_mb_tree = 0;
        }
        // ...
```

- 除tune之外，一些资料中同时提到了preset参数（但实测的几个编码器对延迟没什么影响），用于控制编码速度，它也是一组预设策略，同样可以分别指定。参考x264_param_apply_preset。提高编码速度可能会导致码流增大最多至190%以上；相反，降低速度可减小码流最多至40%以下（相对于默认值medium而言）。

## 参考资料

- x264 tune解析: https://blog.csdn.net/daixinmei/article/details/51886850
- x264 preset/tune实现: https://blog.csdn.net/dangxw_/article/details/50974880
- x264 其他参数: https://blog.csdn.net/qq_35703954/article/details/52791298
