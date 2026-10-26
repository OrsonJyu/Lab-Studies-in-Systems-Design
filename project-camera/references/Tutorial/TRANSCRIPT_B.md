# 录音 B：全时段机器转录（英文原语言）

[AI INTERPRETATION] 本文为本地 Whisper Small 机器识别及 AI 标注，不是经人工逐句听审的认证逐字稿。已输入完整音轨，两轮全片识别；正文采用第二轮术语提示识别，不用摘要替代原句。保留重复、语法不完整和模型原有 `[INAUDIBLE]`。没有可靠声纹分离，不能把每个句子准确分配给老师或某位同学。

录音时长：14:50.496。A/B 按用户上传顺序独立计时；不假设两段无缝衔接、没有重叠或覆盖了整场会议。原件路径及哈希见 [处理记录](PROCESSING_STATUS.md)。

- [第二轮原始字幕](working/B_glossary_pass.srt) · [原始文本](working/B_glossary_pass.txt) · [含 token 概率的 JSON](working/B_glossary_pass.json)
- [无术语提示首轮字幕](working/B_full_small.srt) · [首轮文本](working/B_full_small.txt)

标注规则：`〔待核〕` 表示模型文本 token 平均概率低于 0.65，或含模型生成的 `[INAUDIBLE]`。这只是复核线索，不是准确率；未标注的句子也可能识别错误。`〔AI校注〕` 是依据两轮差异或上下文添加的解释，不是录音原话。人名、组号、金额、技术参数和口头相对日期须另核。

## 重点复核位置

- 00:00–00:30：开头句子和先前项目/工具名称识别不稳定，不补全未录到的上下文。
- 01:45–02:05：10 megabit/s 是会议中的举例估计，不是实测码率。
- 05:25–06:10：编码格式讨论存在抢话；H.265、MPEG-4 不应由这段推成同一概念。
- 06:28–06:45：整段复识别的 'We do not have the server' 与前后文及首轮矛盾；存储位置仍应回听，此处不采信孤立否定句。
- 06:42–07:45：旧摄像头品牌/型号不稳定；O-N-V 名称可能为 ONVIF，待产品文档/原声确认。
- 09:00–09:50：热阵列接口及部件名存在误识别；传感器示例软件在会中描述为尚未跑通，不等于本组已完成。
- 10:20–10:36：精度数字含自我修正，不能作为已核实 ±0.5°C 规格。
- 11:42–11:58：重要歧义：整段两轮均出现 stop talking；独立局部复识别 11:50.720–11:52.920 为 start talking。后文讨论协调，纪要采用“开始沟通”的待核解读，不将单词修正冒充人工听审。
- 13:28–14:07：assignment two/three、two weeks 和 scope 存在口误/误识别；正式截止日期以作业原页为准。

## 全文

### 00:00

**[00:00:00,000 → 00:00:15,440]** 〔待核〕 My previous piece is actually from 2D image to feed a depth of petal, to predict the depth

**[00:00:15,440 → 00:00:24,800]** 〔待核〕 of the image, and then through analysis, it tells you how close you are related to the

**[00:00:24,800 → 00:00:25,800]** bird.

**[00:00:25,800 → 00:00:30,960]** This one essentially is the game engine that can run on browser.

**[00:00:30,960 → 00:00:33,200]** So I used to use this, we have a project.

**[00:00:33,200 → 00:00:36,440]** So this one is free, I like to use free things.

**[00:00:36,440 → 00:00:42,080]** Unity is actually too expensive, I mean not computational expensive, it's not money.

**[00:00:42,080 → 00:00:43,760]** So this one is actually much like ways.

**[00:00:43,760 → 00:00:49,560]** So theoretically speaking, you can have a 3D space, 3D model and show the path that is

**[00:00:49,560 → 00:00:53,840]** moving, theoretically speaking, but of course it takes a lot of time, but I'm not expecting

**[00:00:53,840 → 00:00:54,840]** to do that.

**[00:00:54,840 → 00:01:00,400]** So actually you can, if you would like to explore, you can let me know.

### 01:00

**[00:01:00,400 → 00:01:06,680]** But basically I think these are already very useful information, it's actually up to, because

**[00:01:06,680 → 00:01:11,400]** from the school perspective and the student perspective, they do not expect it to be very

**[00:01:11,400 → 00:01:12,400]** sophisticated.

**[00:01:12,400 → 00:01:17,520]** So even as simple as just a video recording, it's already good enough.

**[00:01:17,520 → 00:01:24,680]** But of course if you have some analytics indicating about the movement, maybe it can be processed

**[00:01:24,680 → 00:01:25,680]** later on.

**[00:01:25,680 → 00:01:30,840]** But you have to record the data, you run it through another GPU or maybe a PC to record

**[00:01:30,840 → 00:01:35,000]** the data and then you can retrieve the images, I think it's already good enough.

**[00:01:35,000 → 00:01:42,160]** So do we really need an SSD, because if we want to analyze the data later, and then...

**[00:01:42,160 → 00:01:47,280]** Oh you still have to store it, you still have to store it, it's very huge.

**[00:01:47,280 → 00:01:52,600]** Now if you didn't do the processing in real time, you do not know where there are any

**[00:01:52,600 → 00:01:53,600]** activity.

**[00:01:53,600 → 00:01:55,000]** 〔待核〕 So you have to have a full stream.

**[00:01:55,000 → 00:02:02,800]** So understanding is about maybe 10 megabit per second, so if you run it for one day it's

### 02:00

**[00:02:02,800 → 00:02:03,800]** already huge.

**[00:02:03,800 → 00:02:04,800]** 〔待核〕 Yeah.

**[00:02:04,800 → 00:02:07,160]** So that's why SSD may be better.

**[00:02:07,160 → 00:02:13,280]** Now even better is that you can use, like the TV link, is that it record on activity.

**[00:02:13,280 → 00:02:15,440]** So whenever there's activity, you just record the time.

**[00:02:15,440 → 00:02:20,520]** But then of course if you're doing that, then it depends on the movement, whether it's rich

**[00:02:20,520 → 00:02:23,880]** enough to trigger the movement.

**[00:02:23,880 → 00:02:29,160]** There are some other real situation problems, that's lighting, for example.

**[00:02:29,160 → 00:02:34,080]** Because the daytime, the lighting of the environment may be a little bit different, although this

**[00:02:34,080 → 00:02:40,120]** camera is a bit of a night vision, but then when the IR camera turns on, the color will

**[00:02:40,120 → 00:02:41,120]** be different.

**[00:02:41,120 → 00:02:42,120]** 〔待核〕 Yeah.

**[00:02:42,120 → 00:02:48,440]** Even, this is why I remember it's low light, so even when you look at the camera, these

**[00:02:48,440 → 00:02:53,600]** were being taken at night, which actually TV link is really good, but still, you can

**[00:02:53,600 → 00:02:58,640]** see the green color, green hue, right, at night, daytime is different.

**[00:02:58,640 → 00:03:03,000]** So that's why, but if you're using image difference, it should be all no problem, because you're

### 03:00

**[00:03:03,000 → 00:03:07,120]** subtracting from previous frame, because this camera is not moving.

**[00:03:07,120 → 00:03:11,440]** That's why moving, I don't expect it to work, because moving it will be very difficult.

**[00:03:11,440 → 00:03:12,440]** Yeah.

**[00:03:12,440 → 00:03:13,440]** 〔待核〕 Yeah.

**[00:03:13,440 → 00:03:14,440]** 〔待核〕 Do image contraction, right.

**[00:03:14,440 → 00:03:17,360]** Yeah, but those are simple image problems.

**[00:03:17,360 → 00:03:20,400]** You can use OpenCV, but OpenCV is very slow.

**[00:03:20,400 → 00:03:28,080]** If you're using the ROG5, ABI, they have real time image motion tracking, motion recognition,

**[00:03:28,080 → 00:03:40,080]** so if we need the SSP, do we need SSP storage, if we need, we need to buy a brand new one?

**[00:03:40,080 → 00:03:41,080]** I can buy.

**[00:03:41,080 → 00:03:42,080]** Okay.

**[00:03:42,080 → 00:03:49,280]** So actually, I check it is not expensive, but first we are not talking about PC gray SSD.

**[00:03:49,280 → 00:03:54,880]** We are talking about low speed, and so it is not expensive.

**[00:03:54,880 → 00:03:55,880]** 〔待核〕 Low speed.

**[00:03:55,880 → 00:03:56,880]** 〔待核〕 Yeah.

**[00:03:56,880 → 00:04:01,840]** I don't even know if there's an SSD for that.

### 04:00

**[00:04:01,840 → 00:04:03,840]** It's not supposed to be very expensive.

**[00:04:03,840 → 00:04:06,440]** This one is already very expensive, let me check.

**[00:04:06,440 → 00:04:14,280]** This company is already quite expensive, because it's ... I don't know.

**[00:04:14,280 → 00:04:17,200]** Let me check, let me check.

**[00:04:17,200 → 00:04:18,200]** Okay.

**[00:04:18,200 → 00:04:19,200]** It shouldn't be very expensive.

**[00:04:19,200 → 00:04:22,280]** Actually, SSD is easier than half drive.

**[00:04:22,280 → 00:04:23,280]** Yeah.

**[00:04:23,280 → 00:04:24,280]** 〔待核〕 Half drive unit.

**[00:04:24,280 → 00:04:29,080]** But I think, no, I discussed with the school, the school also have a PC.

**[00:04:29,080 → 00:04:37,560]** We can have ... We can actually use a standard PC, maybe an i7, this is one 32-bit memory,

**[00:04:37,560 → 00:04:38,560]** 〔待核〕 red, right?

**[00:04:38,560 → 00:04:39,560]** 〔待核〕 Yeah.

**[00:04:39,560 → 00:04:41,600]** It's actually quite good.

**[00:04:41,600 → 00:04:42,600]** 〔待核〕 Yeah.

**[00:04:42,600 → 00:04:47,480]** If we are using a notebook, we can't keep on running it for 24 hours.

**[00:04:47,480 → 00:04:48,480]** Yes.

**[00:04:48,480 → 00:04:49,480]** Yeah.

**[00:04:49,480 → 00:04:50,480]** 〔待核〕 Yeah.

**[00:04:50,480 → 00:04:51,480]** 〔待核〕 It's so fresh, right?

**[00:04:51,480 → 00:04:52,480]** So that's why using an investment is easier.

**[00:04:52,480 → 00:04:57,000]** So that's why, at the very beginning, we can actually start from using PC first.

**[00:04:57,000 → 00:04:58,000]** Okay.

**[00:04:58,000 → 00:05:02,320]** So for Rock 5, if you are interested to explore it, then I can buy it.

### 05:00

**[00:05:02,320 → 00:05:05,960]** If no, then I will not buy it, because it's a waste of resources.

**[00:05:05,960 → 00:05:06,960]** 〔待核〕 Yes.

**[00:05:06,960 → 00:05:07,960]** 〔待核〕 Yeah.

**[00:05:07,960 → 00:05:08,960]** But the SSD is useful.

**[00:05:08,960 → 00:05:09,960]** Yeah.

**[00:05:09,960 → 00:05:13,880]** Actually, even the whole web can run on Rock 5.

**[00:05:13,880 → 00:05:15,800]** The Rock 5 is actually quite powerful.

**[00:05:15,800 → 00:05:16,800]** Yeah.

**[00:05:16,800 → 00:05:19,000]** So, well, let me just clarify.

**[00:05:19,000 → 00:05:29,720]** It's like, because there are real-time capturing and analyzing on the camera, but the camera

**[00:05:29,720 → 00:05:33,280]** also recording video clips, right?

**[00:05:33,280 → 00:05:34,280]** Yeah.

**[00:05:34,280 → 00:05:42,200]** So, if we need that video clips, we need to store the video clips first on our PC.

**[00:05:42,200 → 00:05:43,200]** 〔待核〕 Yeah.

**[00:05:43,200 → 00:05:44,200]** Yeah.

**[00:05:44,200 → 00:05:45,200]** Yeah.

**[00:05:45,200 → 00:05:49,160]** So, the video clips are already in H.265.

**[00:05:49,160 → 00:05:50,160]** H.265.

**[00:05:50,160 → 00:05:51,160]** 〔待核〕 I know.

**[00:05:51,160 → 00:05:52,160]** 〔待核〕 I know.

**[00:05:52,160 → 00:05:53,160]** 〔待核〕 It's already included.

**[00:05:53,160 → 00:05:54,160]** 〔待核〕 I'm not familiar with it.

**[00:05:54,160 → 00:05:55,160]** 〔待核〕 There's a redial from the standard.

**[00:05:55,160 → 00:05:56,160]** 〔待核〕 What do you want?

**[00:05:56,160 → 00:05:57,160]** H.265.

**[00:05:57,160 → 00:05:59,160]** It's a format, right?

**[00:05:59,160 → 00:06:00,160]** 〔待核〕 MPEG.

### 06:00

**[00:06:00,160 → 00:06:01,160]** Oh, yeah.

**[00:06:01,160 → 00:06:02,160]** MPEG 4.

**[00:06:02,160 → 00:06:03,160]** MPEG 4.

**[00:06:03,160 → 00:06:04,680]** But it's specific and coding.

**[00:06:04,680 → 00:06:05,680]** Yeah.

**[00:06:05,680 → 00:06:07,400]** This one is already supporting H.265.

**[00:06:07,400 → 00:06:08,400]** Okay.

**[00:06:08,400 → 00:06:16,680]** So, it's actually, I think it's an RTSP protocol, and then it transfers the video directly to

**[00:06:16,680 → 00:06:17,680]** the server.

**[00:06:17,680 → 00:06:20,120]** And then on the server, you just store it, right?

**[00:06:20,120 → 00:06:21,600]** This is a video stream.

**[00:06:21,600 → 00:06:23,120]** And also, it's not wireless.

**[00:06:23,120 → 00:06:25,080]** It means that it's not going to lose any packet.

**[00:06:25,080 → 00:06:28,640]** Because if you are talking about wireless, it may drop some package.

**[00:06:28,640 → 00:06:29,640]** Okay.

**[00:06:29,640 → 00:06:34,120]** The videos are stored on the server, but not on a local.

**[00:06:34,120 → 00:06:35,120]** No, no, no.

**[00:06:35,120 → 00:06:37,120]** We do not have SD cards here.

**[00:06:37,120 → 00:06:39,120]** We do not have the server.

**[00:06:39,120 → 00:06:40,120]** Oh, God.

**[00:06:40,120 → 00:06:41,120]** That's why it's a network camera.

**[00:06:41,120 → 00:06:44,120]** Yeah, I think that's why it's like the car.

**[00:06:44,120 → 00:06:46,120]** Oh, no, no, no.

**[00:06:46,120 → 00:06:56,600]** Actually, if you are using the one that we mentioned originally, we were using the TP-104C-220.

**[00:06:56,600 → 00:06:59,600]** This is the one that we, I think it's somewhat similar.

**[00:06:59,600 → 00:07:00,600]** Yeah.

### 07:00

**[00:07:00,600 → 00:07:01,600]** What about it?

**[00:07:01,600 → 00:07:03,600]** Would you want to launch it?

**[00:07:03,600 → 00:07:05,920]** Yeah, this one.

**[00:07:05,920 → 00:07:10,320]** And then this one has a local storage, but the problem is that I cannot retrieve the

**[00:07:10,320 → 00:07:11,320]** data.

**[00:07:11,320 → 00:07:12,320]** 〔待核〕 What are you doing?

**[00:07:12,320 → 00:07:13,320]** No, no.

**[00:07:13,320 → 00:07:15,320]** I manually then you have to copy it, right?

**[00:07:15,320 → 00:07:16,320]** 〔待核〕 Yeah.

**[00:07:16,320 → 00:07:17,320]** 〔待核〕 Copy.

**[00:07:17,320 → 00:07:25,160]** Now, this one, there is an API, but people have to do it to get the API in order to retrieve

**[00:07:25,160 → 00:07:26,160]** 〔待核〕 it.

**[00:07:26,160 → 00:07:27,160]** But which is not that good, right?

**[00:07:27,160 → 00:07:31,360]** Now, although it's actually low cost, but if you cannot control it, why do you want to

**[00:07:31,360 → 00:07:32,360]** move it?

**[00:07:32,360 → 00:07:33,360]** This one is easier.

**[00:07:33,360 → 00:07:36,800]** This one supports a standard for the old man.

**[00:07:36,800 → 00:07:37,800]** 〔待核〕 Yeah.

**[00:07:37,800 → 00:07:38,800]** 〔待核〕 It can actually be pretty.

**[00:07:38,800 → 00:07:39,800]** 〔待核〕 Yeah.

**[00:07:39,800 → 00:07:40,800]** I'm not sure whether you have played with this one.

**[00:07:40,800 → 00:07:42,800]** It supports a standard called the O-N-V something.

**[00:07:42,800 → 00:07:44,680]** I haven't played with it.

**[00:07:44,680 → 00:07:45,680]** This one.

**[00:07:45,680 → 00:07:50,620]** Essentially, it's an HGP protocol for you to control this one.

**[00:07:50,620 → 00:07:51,620]** You can retrieve it.

**[00:07:51,620 → 00:07:52,620]** You can start recording.

**[00:07:52,620 → 00:07:53,620]** You can turn on the lights.

**[00:07:53,620 → 00:07:54,620]** Oh, that's good.

**[00:07:54,620 → 00:07:55,620]** That's good.

**[00:07:55,620 → 00:07:56,620]** 〔待核〕 Even the Pentio.

**[00:07:56,620 → 00:07:57,620]** But this one has no Pentio.

**[00:07:57,620 → 00:08:01,120]** This one is cheaper, but this one is not waterproof.

### 08:00

**[00:08:01,120 → 00:08:03,520]** That's why I don't purchase it, too.

**[00:08:03,520 → 00:08:04,520]** This one is another one.

**[00:08:04,520 → 00:08:06,160]** So you can actually visit this website.

**[00:08:06,160 → 00:08:07,320]** I have the links there.

**[00:08:07,320 → 00:08:11,040]** I want to make sure that I also have purchases.

**[00:08:11,040 → 00:08:14,600]** This afternoon or maybe tomorrow, I'm just not trying to work with this one.

**[00:08:14,600 → 00:08:17,040]** This one is running PoE.

**[00:08:17,040 → 00:08:22,820]** So because it based PoE, then you just need Ethernet cable, 48 books, and then you can

**[00:08:22,820 → 00:08:26,600]** already deliver the video on to it.

**[00:08:26,600 → 00:08:27,600]** Okay.

**[00:08:27,600 → 00:08:33,400]** So what I want you to think from a team is that what is the functional requirement?

**[00:08:33,400 → 00:08:37,420]** What is the user experience that a user is supposed to have?

**[00:08:37,420 → 00:08:41,600]** It's not just about the programming part.

**[00:08:41,600 → 00:08:43,600]** Programming technology is important.

**[00:08:43,600 → 00:08:47,800]** That's why your team seems to have more experience in this technology area.

**[00:08:47,800 → 00:08:48,800]** So that's why it's good.

**[00:08:48,800 → 00:08:51,800]** But then, at least my background is also from engineering.

**[00:08:51,800 → 00:08:56,600]** I understand that people may obsess over technology and then forget about why we want to use

**[00:08:56,600 → 00:08:57,600]** 〔待核〕 the design school.

**[00:08:57,600 → 00:09:03,400]** So that's why I also would like you to think about, and also try to monitor this one.

### 09:00

**[00:09:03,400 → 00:09:07,160]** It's easier to use because it's just as per scene.

**[00:09:07,160 → 00:09:15,240]** So now here, I'm asking my technician to actually create the examples.

**[00:09:15,240 → 00:09:20,480]** Actually previously, I appreciate the component directly, but we have to solder the component.

**[00:09:20,480 → 00:09:26,920]** 〔待核〕 But the bottom I share to you just then, the tiny box that I would hit with here.

**[00:09:26,920 → 00:09:32,280]** This one is already the module, it has the component on it, it has all these capacitors

**[00:09:32,280 → 00:09:33,280]** in the system.

**[00:09:33,280 → 00:09:36,400]** But without that, this device can read a lot of noise.

**[00:09:36,400 → 00:09:41,440]** That's why last year, a few weeks ago, I tried that and then I stopped.

**[00:09:41,440 → 00:09:43,320]** So the software is still not working.

**[00:09:43,320 → 00:09:48,120]** So I'm trying to update the whole thing so that it can test it around.

**[00:09:48,120 → 00:09:55,360]** So that's why, supposedly, electronic wise, it shouldn't be a very big problem.

**[00:09:55,360 → 00:09:58,360]** But then the next step is system integration.

**[00:09:58,360 → 00:10:04,840]** So for example, for this one, at least you have to create a case so that it can be placed

### 10:00

**[00:10:04,840 → 00:10:05,840]** easily.

**[00:10:05,840 → 00:10:10,680]** And also maybe you have to work with some other teams because some other teams may also meet

**[00:10:10,680 → 00:10:13,880]** this camera apart from that camera.

**[00:10:13,880 → 00:10:18,400]** That camera is bulky, so it may not be that easy for you to capture a thing.

**[00:10:18,400 → 00:10:22,000]** This one is actually much easier to put it in different places.

**[00:10:22,000 → 00:10:24,880]** But this one is also quite expensive.

**[00:10:24,880 → 00:10:28,960]** This one, of course, is the same as that one.

**[00:10:28,960 → 00:10:29,960]** But this one is very accurate.

**[00:10:29,960 → 00:10:34,240]** I think it's a plus or minus five, a zero point five degree accuracy.

**[00:10:34,240 → 00:10:38,400]** Actually, it's quite quick, but the resolution is low.

**[00:10:38,400 → 00:10:44,680]** So general speaking, all the data we capture will be transferred to the server, and we

**[00:10:44,680 → 00:10:52,720]** can gain data from the server, for example, the watchman and the humidity.

**[00:10:52,720 → 00:10:57,280]** So if you need those information because of some scenario, it will be good for you to

**[00:10:57,280 → 00:11:00,880]** talk about that in a coming presentation.

### 11:00

**[00:11:00,880 → 00:11:07,000]** That's why in assignment number two, I'm expecting to talk about how long it will take each other.

**[00:11:07,000 → 00:11:14,640]** So we need to talk about what data we need in our assignment two presentation to talk

**[00:11:14,640 → 00:11:15,840]** about hours still.

**[00:11:15,840 → 00:11:19,560]** And also, at the same time, what are the usage scenarios?

**[00:11:19,560 → 00:11:27,280]** Like, for example, maybe you want to adjust the thermal camera setting because of the

**[00:11:27,280 → 00:11:31,000]** temperature in the environment, I'm not sure.

**[00:11:31,000 → 00:11:34,640]** Because sometimes the camera, maybe you have to change the sensitivity because the temperature

**[00:11:34,640 → 00:11:35,640]** 〔待核〕 is hot.

**[00:11:35,640 → 00:11:40,480]** So you have to make sure that you can still capture the heat information.

**[00:11:40,480 → 00:11:46,960]** So before assignment two, do we still need to communicate with different routes like,

**[00:11:46,960 → 00:11:49,960]** for example, one to make sure?

**[00:11:49,960 → 00:11:56,080]** I would prefer you to stop talking to them because this week I tried to meet with every

〔AI校注：上句 stop/start 存在关键识别分歧。局部复识别为 start，见[复识别字幕](working/B_coordination_recheck.srt)。请回听 11:46–12:05；本行未擅自改写原始模型输出。〕

**[00:11:56,080 → 00:12:00,880]** team and see what they are doing, whether they understand the score of the work.

### 12:00

**[00:12:00,880 → 00:12:05,080]** And then you can discuss with each of them to understand more on how to coordinate.

**[00:12:05,080 → 00:12:10,520]** But make sure that, like what I mentioned, at least finish the unit test, the module test,

**[00:12:10,520 → 00:12:12,720]** and some basic integration test.

**[00:12:12,720 → 00:12:17,320]** The whole system, in the worst case, I was thinking about, the whole system will be separated

**[00:12:17,320 → 00:12:19,720]** into small, separate modules.

**[00:12:19,720 → 00:12:23,640]** They do not talk to each other in the worst case.

**[00:12:23,640 → 00:12:27,640]** So that's why the database was still supposed to follow all the data.

**[00:12:27,640 → 00:12:35,520]** So yeah, and what else, I think, yeah, yeah, it's like, shall we give an exact number of

**[00:12:35,520 → 00:12:40,280]** what we need before the assignment two or in the assignment three?

**[00:12:40,280 → 00:12:43,840]** I think, firstly, you confirm what you're going to prove first.

**[00:12:43,840 → 00:12:49,280]** And then, because the whole thing, for me, I haven't, some of them I haven't studied,

**[00:12:49,280 → 00:12:51,000]** like for example, the IK camera.

**[00:12:51,000 → 00:12:59,000]** So that's why usually, the workflow is that, after assignment number two, you come up with

**[00:12:59,000 → 00:13:05,880]** a plan, or a plan, that this plan says that, oh, in the coming two weeks, I will start

### 13:00

**[00:13:05,880 → 00:13:10,520]** working on the IK camera, and then one component that you need, because you are just doing

**[00:13:10,520 → 00:13:12,280]** technology investigation.

**[00:13:12,280 → 00:13:17,840]** So for example, for this one, I already have a camera, I'm expecting in the coming two

**[00:13:17,840 → 00:13:23,040]** weeks, if you're starting working on this one, you will use your PC to try, because from

**[00:13:23,040 → 00:13:28,680]** my understanding, this camera, they have some online packages for you to install the software

**[00:13:28,680 → 00:13:33,200]** on your notebook, so they can check whether the IK camera is working.

**[00:13:33,200 → 00:13:37,400]** But you have to set up this one ready, then at least you have the hub, you have a network

**[00:13:37,400 → 00:13:38,400]** hub, right?

**[00:13:38,400 → 00:13:39,400]** I have the hub downstairs.

**[00:13:39,400 → 00:13:43,720]** I also have some of the things, that's why I want to try where the components are suitable

**[00:13:43,720 → 00:13:45,920]** so that I can give it to you.

**[00:13:45,920 → 00:13:51,280]** So maybe, let's say two weeks time, we do the investigation, and we have this assignment

**[00:13:51,280 → 00:13:53,280]** number two, out of number three.

**[00:13:53,280 → 00:13:55,440]** 〔待核〕 So you have to try these sensors?

**[00:13:55,440 → 00:13:59,000]** Yeah, because once you try the sensor, you know what can be done, what cannot be done.

**[00:13:59,000 → 00:14:03,520]** And that's why in assignment number three, you have to revise your score, because the

### 14:00

**[00:14:03,520 → 00:14:07,480]** score may be, maybe at the end, you'll find out, oh, I can actually put 10 cameras there,

**[00:14:07,480 → 00:14:11,640]** or maybe I can't even put one camera on.

**[00:14:11,640 → 00:14:16,880]** Or for example, another possibility is that you would like to use the TV-link camera,

**[00:14:16,880 → 00:14:20,080]** because this camera is not working, but you still have the camera.

**[00:14:20,080 → 00:14:25,080]** But then, you have to solve the problem that he mentioned, how can you retrieve the image

**[00:14:25,080 → 00:14:33,720]** camera in a less manual way, I don't know how, actually, maybe it's possible, but it

**[00:14:33,720 → 00:14:38,520]** seems that it's not proprietary, because the body is there.

**[00:14:38,520 → 00:14:42,240]** Okay, thank you, thank you, thank you.

**[00:14:42,240 → 00:14:43,960]** Thank you, thank you.

**[00:14:43,960 → 00:14:49,600]** So try to go home, and then let me know, if you have any questions, we'll see you guys.

## 片尾边界说明

完整音轨已处理，但语音模型可能把片尾时间估到文件之外，也可能不为末尾短暂停顿输出文字；这不是录像外存在额外发言的证据。原始时间戳保留以便追溯。
