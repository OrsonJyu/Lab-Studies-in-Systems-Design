# 录音 A：全时段机器转录（英文原语言）

[AI INTERPRETATION] 本文为本地 Whisper Small 机器识别及 AI 标注，不是经人工逐句听审的认证逐字稿。已输入完整音轨，两轮全片识别；正文采用第二轮术语提示识别，不用摘要替代原句。保留重复、语法不完整和模型原有 `[INAUDIBLE]`。没有可靠声纹分离，不能把每个句子准确分配给老师或某位同学。

录音时长：37:55.883。A/B 按用户上传顺序独立计时；不假设两段无缝衔接、没有重叠或覆盖了整场会议。原件路径及哈希见 [处理记录](PROCESSING_STATUS.md)。

- [第二轮原始字幕](working/A_glossary_pass.srt) · [原始文本](working/A_glossary_pass.txt) · [含 token 概率的 JSON](working/A_glossary_pass.json)
- [无术语提示首轮字幕](working/A_full_small.srt) · [首轮文本](working/A_full_small.txt)

标注规则：`〔待核〕` 表示模型文本 token 平均概率低于 0.65，或含模型生成的 `[INAUDIBLE]`。这只是复核线索，不是准确率；未标注的句子也可能识别错误。`〔AI校注〕` 是依据两轮差异或上下文添加的解释，不是录音原话。人名、组号、金额、技术参数和口头相对日期须另核。

## 重点复核位置

- 01:20–02:10：组号、专业缩写和 enclosure/vivarium 有误识别；不能用这段确认团队身份。
- 07:10–07:45：涉及金额：机器识别出现 $300、$160 等。币种、用途、审批未核实，不作采购预算。
- 08:00–09:25：H2265 / UEC / I squared C 等技术名词有误识别可能；H.265、UVC、I²C 只是校读候选，原文保留。
- 19:10–19:40：短句及说话人切换不清，自动化范围以相邻完整讨论理解，不据孤立短句下结论。
- 21:15–22:05：数据库名称多次不稳定（mobile/long DB 等），可能为 MongoDB，但不得当作已定选型。
- 26:05–26:50：week eight 等为口头预期，不能转为正式 deadline。
- 31:10–32:25：行为异常讨论不是兽医诊断规则，不应把停留过久直接判为患病。
- 34:30–35:30：芯片能力、流数量和 NVR/缩写待核；不是已完成的性能测试。
- 37:00–38:00：结尾存在抢话和句子截断，末段 ASR 时间略超出片尾。

## 全文

### 00:00

**[00:00:00,000 → 00:00:10,680]** So you understand the project requirement?

**[00:00:10,680 → 00:00:15,480]** Yeah, to be honest, we roughly review the request.

**[00:00:15,480 → 00:00:22,200]** But I think the main part is to communicate with team one,

**[00:00:22,200 → 00:00:27,240]** because we take responsibility of the whole system's camera.

**[00:00:27,240 → 00:00:28,360]** Yeah, yeah, yeah.

**[00:00:28,360 → 00:00:33,000]** So let me-- because when I met with two other teams,

**[00:00:33,000 → 00:00:36,680]** three other teams yesterday, firstly,

**[00:00:36,680 → 00:00:39,520]** about the requirement for the assignment tool first, right?

**[00:00:39,520 → 00:00:41,520]** Now, because this whole project--

**[00:00:41,520 → 00:00:43,520]** actually, it's also reflected here--

**[00:00:43,520 → 00:00:47,320]** is that I would like each team to provide specific details

**[00:00:47,320 → 00:00:49,680]** on what your project is supposed to be doing,

**[00:00:49,680 → 00:00:54,960]** because what I list out is just a technical requirement.

**[00:00:54,960 → 00:00:57,040]** But then there may be some other thing

**[00:00:57,040 → 00:00:58,680]** that you would like to fill in.

**[00:00:58,680 → 00:01:03,440]** So that's why I would also like you to revise, extend.

### 01:00

**[00:01:03,440 → 00:01:05,840]** For example, something if it's too difficult for you,

**[00:01:05,840 → 00:01:07,680]** then you'd let me know.

**[00:01:07,680 → 00:01:10,920]** Because there are always alternatives, right?

**[00:01:10,920 → 00:01:12,200]** Other solutions, right?

**[00:01:12,200 → 00:01:15,440]** And also, elaborate how your project scope is related

**[00:01:15,440 → 00:01:17,080]** to the project goal, which is something

**[00:01:17,080 → 00:01:20,040]** that I will talk about quickly, this one, right?

**[00:01:20,040 → 00:01:23,360]** And also, playing on technical inspiration,

**[00:01:23,360 → 00:01:25,440]** state clearly who is responsible a lot,

**[00:01:25,440 → 00:01:28,520]** and also elaborate how you are expected

**[00:01:28,520 → 00:01:30,240]** to collaborate with others, right?

**[00:01:30,240 → 00:01:33,880]** Now, yesterday I met with team six.

**[00:01:33,880 → 00:01:36,000]** 〔待核〕 They are working on the end brochure.

**[00:01:36,000 → 00:01:40,480]** So OK, team six, team six.

**[00:01:40,480 → 00:01:42,120]** - So they are working on the project one, right?

**[00:01:42,120 → 00:01:43,040]** - Probably one, yeah.

**[00:01:43,040 → 00:01:47,880]** So actually, there will be five students, three of them

**[00:01:47,880 → 00:01:51,160]** from TED, one is from SSD, and the other one

**[00:01:51,160 → 00:01:53,480]** is actually from IBD.

**[00:01:53,480 → 00:01:57,040]** So the IBD students have a product design background,

**[00:01:57,040 → 00:01:58,480]** industry design background.

**[00:01:58,480 → 00:02:02,000]** So the three TED, architecture background, landscaping.

### 02:00

**[00:02:02,000 → 00:02:05,400]** And also, one more is on the SSD is on use experience,

**[00:02:05,400 → 00:02:08,240]** which actually is quite a good combination.

**[00:02:08,240 → 00:02:11,520]** So I'll talk about the final project first,

**[00:02:11,520 → 00:02:15,560]** because I want to exhibit a bit on the context,

**[00:02:15,560 → 00:02:16,560]** the background of the project.

**[00:02:16,560 → 00:02:18,760]** Because in the background, I have already elaborate,

**[00:02:18,760 → 00:02:21,920]** but it seems like some students don't maybe misunderstood

**[00:02:21,920 → 00:02:25,360]** or maybe don't quite clear on what they expect to do.

**[00:02:25,360 → 00:02:28,320]** So because the whole thing that we are going to do

**[00:02:28,320 → 00:02:32,840]** is to create a smart IoT for GECO, to facilitate students,

**[00:02:32,840 → 00:02:34,600]** facilitate students, right?

**[00:02:34,600 → 00:02:40,240]** So yesterday, one student from team six,

**[00:02:40,240 → 00:02:45,520]** she asked me, who is the expected user?

**[00:02:45,520 → 00:02:49,800]** And also, how are these supposed to use the system?

**[00:02:49,800 → 00:02:54,560]** So my answer to them is that, firstly, this system

**[00:02:54,560 → 00:02:58,200]** will be used in primary and secondary schools.

**[00:02:58,200 → 00:02:59,960]** Mostly, it will be in primary school

**[00:02:59,960 → 00:03:01,680]** and also maybe in secondary school.

### 03:00

**[00:03:01,680 → 00:03:06,480]** So we have to understand the situation in these schools.

**[00:03:06,480 → 00:03:09,400]** So usually, in these schools, they

**[00:03:09,400 → 00:03:13,400]** have specialized people taking care of the GECO.

**[00:03:13,400 → 00:03:17,800]** So for example, I met with, for example, this one.

**[00:03:17,800 → 00:03:21,480]** So this one is simply in crucial project description.

**[00:03:21,480 → 00:03:27,960]** So we have installed a invariant enclosure

**[00:03:27,960 → 00:03:31,040]** in their secondary and primary school.

**[00:03:31,040 → 00:03:33,160]** And then usually, the teachers, the students

**[00:03:33,160 → 00:03:36,920]** will come at some specific time in a day.

**[00:03:36,920 → 00:03:39,680]** So maybe during the weekday, Monday to Friday.

**[00:03:39,680 → 00:03:42,680]** And then maybe during the recess time,

**[00:03:42,680 → 00:03:55,160]** they have 15 minutes for them to actually come over here

**[00:03:55,160 → 00:03:57,280]** and then maybe do some simple thing.

**[00:03:57,280 → 00:04:01,040]** Like, for example, check the GECO and also

### 04:00

**[00:04:01,040 → 00:04:02,440]** do some simple thing, right?

**[00:04:02,440 → 00:04:03,960]** But actually, most of the time, they

**[00:04:03,960 → 00:04:06,120]** are not going to take care of them.

**[00:04:06,120 → 00:04:09,000]** Because the students, I'm not sure maybe you already

**[00:04:09,000 → 00:04:10,760]** have some similar experience.

**[00:04:10,760 → 00:04:13,000]** Suppose that you were studying in secondary school and primary

**[00:04:13,000 → 00:04:13,720]** school.

**[00:04:13,720 → 00:04:17,720]** So this is more like an equipment in an embroidery.

**[00:04:17,720 → 00:04:20,120]** So someone will take care of the equipment, not you.

**[00:04:20,120 → 00:04:24,920]** But you will come as a student to try to do something else,

**[00:04:24,920 → 00:04:27,480]** right, after your learning experience.

**[00:04:27,480 → 00:04:29,800]** So that's why it is important to understand

**[00:04:29,800 → 00:04:33,480]** if we talk about what are they supposed to do,

**[00:04:33,480 → 00:04:36,240]** what are the students supposed to do.

**[00:04:36,240 → 00:04:39,560]** Actually, the students are more like having fun, right?

**[00:04:39,560 → 00:04:43,400]** So that's why for this IoT system,

**[00:04:43,400 → 00:04:46,520]** we actually suppose that the system is mostly

**[00:04:46,520 → 00:04:50,800]** used by, for example, the workers or maybe the teachers.

**[00:04:50,800 → 00:04:55,320]** Some other, maybe some specific students.

**[00:04:55,320 → 00:04:58,840]** So in our kidneys, we are collaborating

**[00:04:58,840 → 00:05:01,080]** with the secondary school.

### 05:00

**[00:05:01,080 → 00:05:04,520]** Actually, my original plan is that we

**[00:05:04,520 → 00:05:08,000]** will develop a system for the secondary school students.

**[00:05:08,000 → 00:05:12,080]** So they get familiar with how to work with this system.

**[00:05:12,080 → 00:05:14,440]** And then later on in the next semester,

**[00:05:14,440 → 00:05:17,720]** starting from January, which made, definitely,

**[00:05:17,720 → 00:05:19,680]** you will not be involved because you are not

**[00:05:19,680 → 00:05:22,600]** in this project anymore, because in the second semester,

**[00:05:22,600 → 00:05:23,960]** you will work on something.

**[00:05:23,960 → 00:05:26,800]** So they will actually work with the primary school students

**[00:05:26,800 → 00:05:32,000]** to help them to make use of the system for their learning.

**[00:05:32,000 → 00:05:33,440]** Now, so that's one thing.

**[00:05:33,440 → 00:05:38,760]** So in the first semester, at least for the secondary school,

**[00:05:38,760 → 00:05:40,920]** one thing that I would like you to think about

**[00:05:40,920 → 00:05:44,040]** is how can we get all these sensors into it?

**[00:05:44,040 → 00:05:47,520]** How can it facilitate them to learn science and technology?

**[00:05:47,520 → 00:05:51,680]** So for example, let's say I have one project on high.

**[00:05:51,680 → 00:05:55,520]** Let's say, for example, I want to control the temperature.

**[00:05:55,520 → 00:05:57,120]** And then I think you have seen this one.

**[00:05:57,120 → 00:05:59,800]** I want to control the temperature and humidity

**[00:05:59,800 → 00:06:01,480]** so as to see their behavior.

### 06:00

**[00:06:01,480 → 00:06:05,160]** So the whole project is actually more on recording their behavior.

**[00:06:05,160 → 00:06:06,680]** So then we can analyze it.

**[00:06:06,680 → 00:06:08,880]** So that's why it's important.

**[00:06:08,880 → 00:06:11,520]** We understand from the user perspective

**[00:06:11,520 → 00:06:17,760]** what they may potentially benefit because of your project.

**[00:06:17,760 → 00:06:20,480]** So that's why we have to be clear about that.

**[00:06:20,480 → 00:06:25,000]** So for this one, actually, requirement-wise,

**[00:06:25,000 → 00:06:28,280]** what our original thing about is that it's actually

**[00:06:28,280 → 00:06:31,400]** good for them for us to have some recording system.

**[00:06:31,400 → 00:06:34,040]** So that we can record what's actually happening.

**[00:06:34,040 → 00:06:36,880]** So it's more like an activity measurement.

**[00:06:36,880 → 00:06:39,880]** So I have already provided a link here.

**[00:06:39,880 → 00:06:43,920]** So this one, we just purchased it from Taobao.

**[00:06:43,920 → 00:06:48,680]** So if you find some other things that are more suitable,

**[00:06:48,680 → 00:06:49,200]** let me know.

**[00:06:49,200 → 00:06:51,720]** Because actually, I will help you to buy it

**[00:06:51,720 → 00:06:55,560]** because I want to make sure that we have a check on whether

**[00:06:55,560 → 00:06:58,320]** the components are appropriate for you.

**[00:06:58,320 → 00:07:00,600]** This one is an IP card.

### 07:00

**[00:07:00,600 → 00:07:02,200]** It needs a cable.

**[00:07:02,200 → 00:07:03,480]** I can find cable.

**[00:07:03,480 → 00:07:05,360]** And also, it is PoE.

**[00:07:05,360 → 00:07:07,800]** So that's why it's also waterproof.

**[00:07:07,800 → 00:07:11,080]** So that's why for this particular project,

**[00:07:11,080 → 00:07:14,520]** because you can actually go to this link.

**[00:07:14,520 → 00:07:16,400]** I'm not sure whether you can see this page.

**[00:07:16,400 → 00:07:21,840]** This is a company that you can buy from this website.

**[00:07:21,840 → 00:07:24,720]** But most of the expensive material I would buy from you.

**[00:07:24,720 → 00:07:27,440]** But then if you want to buy something else,

**[00:07:27,440 → 00:07:29,160]** you still have the budget.

**[00:07:29,160 → 00:07:34,960]** Actually, I think they are $300 from the program.

**[00:07:34,960 → 00:07:36,440]** And you can actually purchase it.

**[00:07:36,440 → 00:07:40,040]** If you want more money because of some reason, let me know.

**[00:07:40,040 → 00:07:42,320]** So this one is actually not that expensive.

**[00:07:42,320 → 00:07:43,320]** 〔待核〕 It's $160.

**[00:07:43,320 → 00:07:45,360]** So for this one, I'm not sure whether you

**[00:07:45,360 → 00:07:47,320]** have played with this one.

**[00:07:47,320 → 00:07:50,440]** Because this project is actually more technically oriented.

**[00:07:50,440 → 00:07:52,760]** So that's why I checked the program.

**[00:07:52,760 → 00:07:54,760]** It seems like you are more suitable for--

**[00:07:54,760 → 00:07:57,560]** actually, you have to experience it.

**[00:07:57,560 → 00:07:58,880]** So that's why I want to know more.

**[00:07:58,880 → 00:08:01,480]** Originally, I was planning to use this one.

### 08:00

**[00:08:01,480 → 00:08:04,640]** But I found that maybe using this one is easier.

**[00:08:04,640 → 00:08:06,040]** Because it's already--

**[00:08:06,040 → 00:08:08,640]** 〔待核〕 has the H2265 encoding.

**[00:08:08,640 → 00:08:11,480]** It's already doing the encoding on it.

**[00:08:11,480 → 00:08:16,120]** So this one, you still need P4 to do the encoding.

**[00:08:16,120 → 00:08:17,800]** And also, the throughput is not that hard.

**[00:08:17,800 → 00:08:18,560]** They're not going to be good.

**[00:08:18,560 → 00:08:20,760]** And also, we can use UEC camera.

**[00:08:20,760 → 00:08:22,760]** But the problem with UEC is that we

**[00:08:22,760 → 00:08:24,000]** do not have a waterproof one.

**[00:08:24,000 → 00:08:25,520]** This one is already waterproof.

**[00:08:25,520 → 00:08:27,080]** So that's why it's already good enough.

**[00:08:27,080 → 00:08:30,280]** So we don't have to care too many things.

**[00:08:30,280 → 00:08:33,840]** So basically, for technically speaking, I'm expecting two.

**[00:08:33,840 → 00:08:34,560]** One is this one.

**[00:08:34,560 → 00:08:36,520]** The other one is a thermal camera.

**[00:08:36,520 → 00:08:41,040]** So thermal camera is this one.

**[00:08:41,040 → 00:08:44,800]** I need to check it before I can talk to you for this one.

**[00:08:44,800 → 00:08:46,760]** I'm not sure whether you have played with this one.

**[00:08:46,760 → 00:08:52,560]** This one is actually very simple.

**[00:08:52,560 → 00:08:55,160]** It's just nice for this one.

**[00:08:55,160 → 00:08:57,280]** You can actually go online.

**[00:08:57,280 → 00:09:01,200]** 〔待核〕 I did some trial, but it's only two years ago.

### 09:00

**[00:09:01,200 → 00:09:02,080]** Somewhat like that.

**[00:09:02,080 → 00:09:02,560]** 〔待核〕 Yeah.

**[00:09:02,560 → 00:09:06,560]** So it's not quite accurate.

**[00:09:06,560 → 00:09:10,640]** Yeah, I think it's OK because we are just checking temperature.

**[00:09:10,640 → 00:09:12,720]** Also, the resolution is not good.

**[00:09:12,720 → 00:09:15,400]** But the advantage is that we can measure

**[00:09:15,400 → 00:09:19,360]** the temperature of the gank hole relatively quickly

**[00:09:19,360 → 00:09:21,480]** as compared to the camera camera.

**[00:09:21,480 → 00:09:23,160]** The camera cannot, right?

**[00:09:23,160 → 00:09:25,960]** So that's the original idea.

**[00:09:25,960 → 00:09:29,280]** But of course, if you have some other ideas,

**[00:09:29,280 → 00:09:32,080]** I'm happy to know what.

**[00:09:32,080 → 00:09:38,080]** And also, you will have to interface with the volume design.

**[00:09:38,080 → 00:09:42,640]** Actually, I'm expecting you, because of all the enclosure

**[00:09:42,640 → 00:09:45,400]** projects, just creating the enclosure.

**[00:09:45,400 → 00:09:47,680]** So yesterday, I also discussed with them,

**[00:09:47,680 → 00:09:50,640]** maybe they will focus more on creating

**[00:09:50,640 → 00:09:54,600]** the more like a LEGO system, so that they can combine,

**[00:09:54,600 → 00:09:59,440]** create this one, so that they can customize it later on.

**[00:09:59,440 → 00:10:03,160]** So for this one, I think a very important concept

### 10:00

**[00:10:03,160 → 00:10:08,960]** for the whole project is just recorded in Richmond.

**[00:10:08,960 → 00:10:12,840]** So now, because this project is not just

**[00:10:12,840 → 00:10:16,560]** about technology, I think, because of the design school.

**[00:10:16,560 → 00:10:18,880]** That's why we also have to understand

**[00:10:18,880 → 00:10:20,360]** why we have to do this.

**[00:10:20,360 → 00:10:22,000]** Now, actually, if you're interested,

**[00:10:22,000 → 00:10:24,640]** you can refer to this page.

**[00:10:24,640 → 00:10:25,840]** This page is called Richmond.

**[00:10:25,840 → 00:10:29,600]** Now, the concept of Richmond, I think, is more maybe.

**[00:10:29,600 → 00:10:31,840]** It's sort of easier to understand.

**[00:10:31,840 → 00:10:34,560]** Is that-- now, why Richmond?

**[00:10:34,560 → 00:10:37,600]** So the concept of Richmond is to keep that.

**[00:10:37,600 → 00:10:39,960]** Enrichment is something that helps

**[00:10:39,960 → 00:10:42,640]** to keep the gank hole happy, right?

**[00:10:42,640 → 00:10:44,200]** Because they are in captive, right?

**[00:10:44,200 → 00:10:45,760]** So you want to-- like, for example,

**[00:10:45,760 → 00:10:49,160]** if you keep a cat, for example, at home,

**[00:10:49,160 → 00:10:50,960]** you want to keep it-- make it happy, right?

**[00:10:50,960 → 00:10:52,240]** So same, right?

**[00:10:52,240 → 00:10:54,520]** So basically, these are-- this video, I think,

**[00:10:54,520 → 00:10:55,120]** is quite good.

**[00:10:55,120 → 00:10:57,880]** That's why I'll make some notes on what they talk about.

**[00:10:57,880 → 00:10:59,920]** So the idea of the enrichment is that you

**[00:10:59,920 → 00:11:02,280]** want to keep them happy, and also keep them mentally

### 11:00

**[00:11:02,280 → 00:11:05,120]** stimulated, and also physically excised,

**[00:11:05,120 → 00:11:07,120]** and also we've done something for them to explore.

**[00:11:07,120 → 00:11:10,600]** So that's why for team one, team six,

**[00:11:10,600 → 00:11:12,600]** when they're working on this project,

**[00:11:12,600 → 00:11:15,440]** one thing that they need to do is to create maybe

**[00:11:15,440 → 00:11:19,720]** some structure for them to climb around and explore, right?

**[00:11:19,720 → 00:11:21,520]** 〔待核〕 That's what it means, right?

**[00:11:21,520 → 00:11:23,120]** So it doesn't have to be natural looking.

**[00:11:23,120 → 00:11:25,720]** So that's why just team one students ask me

**[00:11:25,720 → 00:11:27,120]** whether it has to be like that.

**[00:11:27,120 → 00:11:29,360]** It can be-- it can be a building, right?

**[00:11:29,360 → 00:11:30,840]** And we're building with many tunnels.

**[00:11:30,840 → 00:11:32,600]** I think it's also OK.

**[00:11:32,600 → 00:11:34,720]** Another thing that-- what they are doing--

**[00:11:34,720 → 00:11:37,160]** planning to do it is to create tunnel system.

**[00:11:37,160 → 00:11:38,600]** So for example, we started a tunnel system

**[00:11:38,600 → 00:11:44,760]** that we tried last semester, last January, two to five.

**[00:11:44,760 → 00:11:48,720]** So maybe we can-- I'm expecting to extend it further.

**[00:11:48,720 → 00:11:51,080]** Now, that's from their perspective.

**[00:11:51,080 → 00:11:53,160]** Now, for your perspective, you may also

**[00:11:53,160 → 00:11:56,280]** think about how to support the whole story, right?

**[00:11:56,280 → 00:11:59,240]** It doesn't have to be just what I put down here, right?

**[00:11:59,240 → 00:12:01,320]** So that's why there's something that I would

### 12:00

**[00:12:01,320 → 00:12:02,680]** like you to think about.

**[00:12:02,680 → 00:12:04,680]** So what was the belief, for example,

**[00:12:04,680 → 00:12:08,240]** is that I was talking to them, is that, for example,

**[00:12:08,240 → 00:12:11,960]** let's say we can put some infrared camera at the back,

**[00:12:11,960 → 00:12:15,240]** right, because when you look at this type of landscape,

**[00:12:15,240 → 00:12:17,480]** some people actually design the landscape in such a way

**[00:12:17,480 → 00:12:22,480]** that this variety of it has the front slope

**[00:12:22,480 → 00:12:24,240]** 〔待核〕 for the gap with the plane.

**[00:12:24,240 → 00:12:27,080]** But at the back, they have some capacity for them

**[00:12:27,080 → 00:12:27,960]** to walk around, right?

**[00:12:27,960 → 00:12:30,840]** So we can actually place some camera at the back

**[00:12:30,840 → 00:12:33,320]** so that while they're exploring, we can also

**[00:12:33,320 → 00:12:37,720]** know where they are and also measure their activities, right?

**[00:12:37,720 → 00:12:43,680]** So it can be optical camera, it can be infrared camera, right?

**[00:12:43,680 → 00:12:46,920]** 〔待核〕 So infrared camera is one expensive.

**[00:12:46,920 → 00:12:49,600]** So that's why maybe it's not easy to have.

**[00:12:49,600 → 00:12:52,360]** So do the multiple cameras, or just one--

**[00:12:52,360 → 00:12:54,640]** Maybe multiple, maybe multiple.

**[00:12:54,640 → 00:12:58,920]** I think that depends on the structure of the case, yeah.

**[00:12:58,920 → 00:13:01,800]** But actually, for last year, what we did

### 13:00

**[00:13:01,800 → 00:13:05,480]** is that we already have two cameras.

**[00:13:05,480 → 00:13:07,640]** So actually, we place one here, and then

**[00:13:07,640 → 00:13:09,720]** we also place another one here.

**[00:13:09,720 → 00:13:12,120]** This one was the initial setup.

**[00:13:12,120 → 00:13:15,600]** So this actually is a TP-linked camera, this one.

**[00:13:15,600 → 00:13:16,960]** It's an IV camera.

**[00:13:16,960 → 00:13:19,400]** So we just use the camera to--

**[00:13:19,400 → 00:13:21,600]** the mobile phone to keep track of--

**[00:13:21,600 → 00:13:24,400]** 〔待核〕 to record the user that we can know.

**[00:13:24,400 → 00:13:28,560]** But actually, the whole thing is that it's not that easy to use,

**[00:13:28,560 → 00:13:31,360]** because I'm-- for example, right now, I'm still running the--

**[00:13:31,360 → 00:13:35,480]** Is it a live camera?

**[00:13:35,480 → 00:13:37,080]** So for example, this one.

**[00:13:37,080 → 00:13:38,360]** This one actually is the camera.

**[00:13:38,360 → 00:13:40,200]** Right now, I'm still running it.

**[00:13:40,200 → 00:13:43,800]** With two kept goes inside, I think.

**[00:13:43,800 → 00:13:46,560]** So I think you should be familiar with the TP-link.

**[00:13:46,560 → 00:13:47,600]** Yeah, yes.

**[00:13:47,600 → 00:13:48,240]** OK.

**[00:13:48,240 → 00:13:50,840]** But of course, this one is a bankage.

**[00:13:50,840 → 00:13:53,800]** It's that we cannot record it.

**[00:13:53,800 → 00:13:55,880]** Can I control the direction?

**[00:13:55,880 → 00:13:56,840]** This one is not.

**[00:13:56,840 → 00:14:00,040]** I think it doesn't need to have control.

### 14:00

**[00:14:00,040 → 00:14:01,400]** The angle is the right angle.

**[00:14:01,400 → 00:14:03,360]** Yeah, yeah, the angle.

**[00:14:03,360 → 00:14:05,960]** You can install more, rather than using camera--

**[00:14:05,960 → 00:14:06,960]** Oh, I see.

**[00:14:06,960 → 00:14:11,400]** If you use a pan-tube, it may be quite not reliable.

**[00:14:11,400 → 00:14:13,080]** It's more like a surveillance system, right?

**[00:14:13,080 → 00:14:14,720]** Yeah, actually, it's a surveillance system.

**[00:14:14,720 → 00:14:19,840]** Now, in this space, it's actually humid, humid, humid,

**[00:14:19,840 → 00:14:21,440]** and also high temperature.

**[00:14:21,440 → 00:14:24,400]** So that's why maybe it's not that good for it

**[00:14:24,400 → 00:14:25,320]** to keep on moving.

**[00:14:25,320 → 00:14:26,600]** Yeah, yeah, yeah.

**[00:14:26,600 → 00:14:30,120]** And also, we are not looking for very, very details.

**[00:14:30,120 → 00:14:33,600]** But of course, the one that I showed you is already good enough.

**[00:14:33,600 → 00:14:35,400]** Actually, this one--

**[00:14:35,400 → 00:14:36,880]** this one is actually coming from the camera.

**[00:14:36,880 → 00:14:38,240]** It's actually quite good resolution.

**[00:14:38,240 → 00:14:38,760]** Yeah, yeah.

**[00:14:38,760 → 00:14:47,080]** So the content is actually on the SD card in the TV link camera.

**[00:14:47,080 → 00:14:49,520]** So that's why right now, I was thinking about maybe you

**[00:14:49,520 → 00:14:52,480]** can use this kind of camera, not wireless.

**[00:14:52,480 → 00:14:53,240]** It's wired.

**[00:14:53,240 → 00:14:55,760]** The one that we were using at the time is wireless.

**[00:14:55,760 → 00:14:58,360]** Wireless is because it's easier to watch it in store.

**[00:14:58,360 → 00:14:59,800]** Because the whole thing, we don't

**[00:14:59,800 → 00:15:01,280]** have to think about how to go wired.

### 15:00

**[00:15:01,280 → 00:15:02,040]** 〔待核〕 Yeah, yeah, yeah, yeah.

**[00:15:02,040 → 00:15:03,840]** 〔待核〕 Wiring.

**[00:15:03,840 → 00:15:04,440]** By that?

**[00:15:04,440 → 00:15:04,940]** 〔待核〕 Yeah.

**[00:15:04,940 → 00:15:08,360]** So this one, now, maybe we have to think about how

**[00:15:08,360 → 00:15:14,040]** to install servers or maybe some embedded device, SPC.

**[00:15:14,040 → 00:15:14,540]** Oh, yeah.

**[00:15:14,540 → 00:15:15,840]** So that's why I was thinking about maybe

**[00:15:15,840 → 00:15:18,040]** 〔待核〕 we could use the Rock 5C.

**[00:15:18,040 → 00:15:20,520]** So this maybe-- this is one suggestion,

**[00:15:20,520 → 00:15:22,720]** but I'm not sure whether you're familiar with it.

**[00:15:22,720 → 00:15:25,200]** So if you're familiar with it, then this one.

**[00:15:25,200 → 00:15:28,200]** So this one, actually--

**[00:15:28,200 → 00:15:30,240]** so I'm trying to get ready the hardware.

**[00:15:30,240 → 00:15:31,720]** 〔待核〕 So OK.

**[00:15:31,720 → 00:15:35,680]** 〔待核〕 [INAUDIBLE]

**[00:15:35,680 → 00:15:39,200]** So the main goal is like using the camera to measure

**[00:15:39,200 → 00:15:40,520]** their activity.

**[00:15:40,520 → 00:15:42,800]** 〔待核〕 Yes, yeah, OK, you're right.

**[00:15:42,800 → 00:15:49,040]** So that's why another thing is that because in this set up,

**[00:15:49,040 → 00:15:51,760]** initially, I'm planning to have one get go.

**[00:15:51,760 → 00:15:54,040]** But it may be more than one get go.

**[00:15:54,040 → 00:15:56,840]** So one thing-- now, firstly, is that I

**[00:15:56,840 → 00:16:01,120]** want to count how often it has movement.

### 16:00

**[00:16:01,120 → 00:16:01,840]** Yeah, yeah.

**[00:16:01,840 → 00:16:04,960]** So now, right now, we have difficulties

**[00:16:04,960 → 00:16:07,280]** in accessing the video.

**[00:16:07,280 → 00:16:10,680]** So it can be caught on motion, but still, we

**[00:16:10,680 → 00:16:13,000]** do not have very good statistics, right?

**[00:16:13,000 → 00:16:14,960]** And also, we cannot retrieve easily the image

**[00:16:14,960 → 00:16:16,680]** so that we do pattern recognition.

**[00:16:16,680 → 00:16:19,960]** For example, if you're using OpenCV,

**[00:16:19,960 → 00:16:22,720]** you have quite a lot of difficulties in retrieving

**[00:16:22,720 → 00:16:24,720]** the audio video.

**[00:16:24,720 → 00:16:26,120]** So that's the first thing.

**[00:16:26,120 → 00:16:28,720]** The second one is about color pattern.

**[00:16:28,720 → 00:16:32,160]** Because the get go, they have different patterns, right?

**[00:16:32,160 → 00:16:35,320]** We can theoretically-- well, actually, not theoretically.

**[00:16:35,320 → 00:16:38,440]** We can actually do some post-processing

**[00:16:38,440 → 00:16:40,080]** to recognize the patterns so that we

**[00:16:40,080 → 00:16:44,160]** know which get go gets to which particular place.

**[00:16:44,160 → 00:16:47,640]** So that's what we'd like to do in the longer run, right?

**[00:16:47,640 → 00:16:51,120]** So right now, we only expect one get go.

**[00:16:51,120 → 00:16:53,720]** But in the future, because the tank is fake,

**[00:16:53,720 → 00:16:55,560]** we can have more than one.

**[00:16:55,560 → 00:17:02,040]** And also, we may place more than one surveillance camera

### 17:00

**[00:17:02,040 → 00:17:03,720]** around the space.

**[00:17:03,720 → 00:17:07,600]** So that's why you may have to talk to the other team.

**[00:17:07,600 → 00:17:09,520]** But I'm not expecting you to--

**[00:17:09,520 → 00:17:11,920]** because each of you should have somewhere

**[00:17:11,920 → 00:17:14,560]** you find a basic scope, right?

**[00:17:14,560 → 00:17:17,560]** So I don't want you to have some scope that are--

**[00:17:17,560 → 00:17:20,040]** and you don't know who is responsible for what, right?

**[00:17:20,040 → 00:17:23,200]** Now, this one, one possibility is that we can actually

**[00:17:23,200 → 00:17:25,920]** 〔待核〕 make-- [INAUDIBLE]

**[00:17:25,920 → 00:17:27,640]** I'll just throw over there.

**[00:17:27,640 → 00:17:29,440]** 〔待核〕 [INAUDIBLE]

**[00:17:29,440 → 00:17:32,200]** So now, so one of the things that--

**[00:17:32,200 → 00:17:34,480]** because I saw a video mentioned about how

**[00:17:34,480 → 00:17:37,200]** to design the verailleur, one possibility

**[00:17:37,200 → 00:17:42,360]** is that they designed a climbing surface, right?

**[00:17:42,360 → 00:17:43,320]** Somewhat like this, right?

**[00:17:43,320 → 00:17:43,880]** Yeah.

**[00:17:43,880 → 00:17:47,080]** And then-- so this is the back, we can actually climb, right?

**[00:17:47,080 → 00:17:49,080]** And then there is some opening.

**[00:17:49,080 → 00:17:51,920]** But at the same time, at the back,

**[00:17:51,920 → 00:17:54,280]** the whole thing is actually open.

**[00:17:54,280 → 00:17:58,880]** You, from a normal person, people will only view from the front.

**[00:17:58,880 → 00:18:01,080]** So that's why, from the gecko perspective,

### 18:00

**[00:18:01,080 → 00:18:03,640]** this is an exposed space.

**[00:18:03,640 → 00:18:06,880]** So for gecko, they are afraid of staying in the exposed way

**[00:18:06,880 → 00:18:08,080]** for a long time.

**[00:18:08,080 → 00:18:10,360]** It's because they want to hide from predator.

**[00:18:10,360 → 00:18:13,160]** So that's why they will usually go in, right?

**[00:18:13,160 → 00:18:15,800]** I saw a video mentioning that they actually

**[00:18:15,800 → 00:18:18,200]** have some opening at the back.

**[00:18:18,200 → 00:18:20,200]** You can actually put a camera there.

**[00:18:20,200 → 00:18:22,720]** You keep the lights theme so that you just

**[00:18:22,720 → 00:18:24,880]** record what's activity inside.

**[00:18:24,880 → 00:18:28,040]** But then they will feel comfortable and safe, right?

**[00:18:28,040 → 00:18:30,600]** So I almost think about at least this setup, right?

**[00:18:30,600 → 00:18:32,920]** So that's why for this setup, maybe

**[00:18:32,920 → 00:18:35,200]** we are talking about two cameras, right?

**[00:18:35,200 → 00:18:36,760]** Or maybe three.

**[00:18:36,760 → 00:18:40,240]** So because we want to provide a setup to that,

**[00:18:40,240 → 00:18:43,320]** students can take care of the gecko.

**[00:18:43,320 → 00:18:45,960]** And also, they can observe the gecko.

**[00:18:45,960 → 00:18:48,560]** So one thing that what I was doing last semester

**[00:18:48,560 → 00:18:51,400]** was that we create some tunnels, right?

**[00:18:51,400 → 00:18:55,040]** And then to see how often they get into a tunnel.

**[00:18:55,040 → 00:18:59,000]** So back to your question, what is the use of the video?

**[00:18:59,000 → 00:19:01,720]** If we can do image processing, let's say OpenCV.

### 19:00

**[00:19:01,720 → 00:19:03,880]** OpenCV is already good enough, right?

**[00:19:03,880 → 00:19:05,440]** But OpenCV is slow.

**[00:19:05,440 → 00:19:07,360]** But anyway, if we have the video,

**[00:19:07,360 → 00:19:09,680]** we can already do quite a lot of image processing.

**[00:19:09,680 → 00:19:10,840]** We can estimate.

**[00:19:10,840 → 00:19:11,840]** We can measure.

**[00:19:11,840 → 00:19:13,360]** For example, there's a tunnel.

**[00:19:13,360 → 00:19:15,560]** It goes in at some particular time.

**[00:19:15,560 → 00:19:19,360]** Goes out at some particular time, the patterns match.

**[00:19:19,360 → 00:19:21,520]** It means that the same gecko, right?

**[00:19:21,520 → 00:19:26,280]** And then we can have analytics and then data.

**[00:19:26,280 → 00:19:29,640]** So what I want to do is a real IoT system, right?

**[00:19:29,640 → 00:19:31,640]** Yes.

**[00:19:31,640 → 00:19:33,440]** 〔待核〕 Automatic for me.

**[00:19:33,440 → 00:19:35,240]** Automatic.

**[00:19:35,240 → 00:19:39,080]** Now for strong things, it's something that you will do later on.

**[00:19:39,080 → 00:19:40,040]** Yeah, in the program.

**[00:19:40,040 → 00:19:42,640]** But the camera is very useful because we still

**[00:19:42,640 → 00:19:45,160]** need to capture the raw data.

**[00:19:45,160 → 00:19:47,360]** So we can do the process.

**[00:19:47,360 → 00:19:53,200]** So basically, how this message was transferred to students?

**[00:19:53,200 → 00:19:55,680]** 〔待核〕 Now, they are using an app or--

**[00:19:55,680 → 00:19:57,560]** It can be as simple as the one that I

**[00:19:57,560 → 00:20:00,840]** 〔待核〕 shown on the using a note read, a web-based interface.

### 20:00

**[00:20:00,840 → 00:20:01,320]** OK.

**[00:20:01,320 → 00:20:06,280]** So we can put the, for example, the message under the,

**[00:20:06,280 → 00:20:08,280]** let's say, camera--

**[00:20:08,280 → 00:20:09,280]** Yeah.

**[00:20:09,280 → 00:20:09,720]** OK.

**[00:20:09,720 → 00:20:12,440]** Now, I also explained to other students,

**[00:20:12,440 → 00:20:17,440]** I mentioned that because when you're working on the whole project,

**[00:20:17,440 → 00:20:21,600]** you need to do some unit tests, and then module tests,

**[00:20:21,600 → 00:20:23,560]** and then integration tests.

**[00:20:23,560 → 00:20:26,640]** And then you need to do some tests, right?

**[00:20:26,640 → 00:20:29,520]** So I would think about that because not many students

**[00:20:29,520 → 00:20:31,160]** have this engineering background.

**[00:20:31,160 → 00:20:34,960]** So the thing is that, for example, let's say I,

**[00:20:34,960 → 00:20:39,200]** from OK for your case, you have a thermal camera.

**[00:20:39,200 → 00:20:41,520]** Let's say I place a thermal camera here.

**[00:20:41,520 → 00:20:42,920]** The basic things that you need to do

**[00:20:42,920 → 00:20:45,240]** is to check whether this unit is working.

**[00:20:45,240 → 00:20:49,280]** So that's why one thing that I expect at the very beginning

**[00:20:49,280 → 00:20:51,640]** is that, at least, you can use, for example,

**[00:20:51,640 → 00:20:53,840]** web software to connect to it and see

**[00:20:53,840 → 00:20:55,480]** whether it's working, retrieving data.

**[00:20:55,480 → 00:20:56,440]** That's level one.

**[00:20:56,440 → 00:20:56,940]** Yeah.

**[00:20:56,940 → 00:20:58,360]** But level two is the module.

**[00:20:58,360 → 00:21:02,120]** That's what you mentioned is that maybe the second level

### 21:00

**[00:21:02,120 → 00:21:05,080]** is that you run the software on the web.

**[00:21:05,080 → 00:21:06,720]** It's on the server side.

**[00:21:06,720 → 00:21:09,920]** So you retrieve the information to the server side.

**[00:21:09,920 → 00:21:14,000]** So that on the server, maybe we just create a tag.

**[00:21:14,000 → 00:21:16,920]** So that's-- but because in Node-RED,

**[00:21:16,920 → 00:21:20,080]** 〔待核〕 you can actually create the [INAUDIBLE]

**[00:21:20,080 → 00:21:22,360]** 〔待核〕 with the [INAUDIBLE] you can switch, right?

**[00:21:22,360 → 00:21:26,280]** So each of the functions can be just one for module tests,

**[00:21:26,280 → 00:21:27,360]** right?

**[00:21:27,360 → 00:21:31,440]** Just for testing whether it can stream the data to the PC.

**[00:21:31,440 → 00:21:32,880]** Because once you're in contact with the PC,

**[00:21:32,880 → 00:21:34,480]** then you can do anything, right?

**[00:21:34,480 → 00:21:37,040]** So I'm expecting this Node-RED because we're using Node-RED

**[00:21:37,040 → 00:21:40,080]** as a hub for connecting things.

**[00:21:40,080 → 00:21:42,080]** So actually, on Node-RED, you can actually

**[00:21:42,080 → 00:21:44,840]** put the data in mobile DB.

**[00:21:44,840 → 00:21:46,960]** So I'm not sure whether you are--

**[00:21:46,960 → 00:21:49,680]** 〔待核〕 [INAUDIBLE]

**[00:21:49,680 → 00:21:52,000]** --long for DB, right?

**[00:21:52,000 → 00:21:55,040]** Or some other database, ProPress or whatever.

**[00:21:55,040 → 00:21:57,120]** So long DB is easier to do.

**[00:21:57,120 → 00:22:01,520]** So we can actually store all the data inside this database.

### 22:00

**[00:22:01,520 → 00:22:03,760]** Now, in your case, we have a video recording.

**[00:22:03,760 → 00:22:04,600]** That's another thing.

**[00:22:04,600 → 00:22:06,960]** But still conceptually speaking, it's just a database.

**[00:22:06,960 → 00:22:12,240]** So-- and then the next thing is that's what you're asked.

**[00:22:12,240 → 00:22:14,440]** What is the-- how the user actually

**[00:22:14,440 → 00:22:16,000]** going to access the information?

**[00:22:16,000 → 00:22:17,920]** Now, that access of information is something

**[00:22:17,920 → 00:22:19,880]** that I would like you to think about.

**[00:22:19,880 → 00:22:21,880]** For example, let's say I want--

**[00:22:21,880 → 00:22:25,440]** I mentioned just then that maybe I want to count how many times

**[00:22:25,440 → 00:22:28,000]** it goes into the tunnel and then goes out of the tunnel.

**[00:22:28,000 → 00:22:31,040]** That's an outer level of application that they have to do,

**[00:22:31,040 → 00:22:31,800]** right?

**[00:22:31,800 → 00:22:33,520]** So I would think about one possibility

**[00:22:33,520 → 00:22:36,280]** is that it depends on your capability, right?

**[00:22:36,280 → 00:22:38,480]** So it can't be an M by itself.

**[00:22:38,480 → 00:22:40,480]** It doesn't have to be look back.

**[00:22:40,480 → 00:22:42,560]** Because in your class, we have students

**[00:22:42,560 → 00:22:44,520]** from different levels of background.

**[00:22:44,520 → 00:22:49,200]** So at least I want each of them can perform something.

**[00:22:49,200 → 00:22:51,520]** Now, for me, in this class, I want students

**[00:22:51,520 → 00:22:55,600]** to at least touch on circuits and better programming, right?

**[00:22:55,600 → 00:22:59,560]** And also, system programming or maybe IoT programming

**[00:22:59,560 → 00:23:02,280]** on the PC side and also web-based database.

### 23:00

**[00:23:02,280 → 00:23:03,040]** That's it.

**[00:23:03,040 → 00:23:05,400]** Now, if you want to do more, it's up to you, right?

**[00:23:05,400 → 00:23:07,480]** But at least I have to declare to you

**[00:23:07,480 → 00:23:10,240]** that make sure that you know what you are doing.

**[00:23:10,240 → 00:23:13,120]** And you have to put down what you want to do first.

**[00:23:13,120 → 00:23:15,120]** That's why that's the time number two, right?

**[00:23:15,120 → 00:23:16,440]** 〔待核〕 So, sorry.

**[00:23:16,440 → 00:23:18,760]** So basically, we do not--

**[00:23:18,760 → 00:23:20,280]** for example, every group would have

**[00:23:20,280 → 00:23:22,640]** every group output itself.

**[00:23:22,640 → 00:23:25,240]** So for example, for the app, if we made an app,

**[00:23:25,240 → 00:23:28,200]** and other group made a website or something,

**[00:23:28,200 → 00:23:33,120]** we-- it is not necessary that we need to use the same--

**[00:23:33,120 → 00:23:34,520]** May not, may not, may not.

**[00:23:34,520 → 00:23:36,520]** Maybe we can think about--

**[00:23:36,520 → 00:23:38,560]** because it's easier to coordinate.

**[00:23:38,560 → 00:23:42,720]** So now, one more thing is that, for example, let's say,

**[00:23:42,720 → 00:23:45,320]** because what some other teams are working on,

**[00:23:45,320 → 00:23:46,120]** 〔待核〕 average of control--

**[00:23:46,120 → 00:23:47,040]** [INTERPOSING VOICES]

**[00:23:47,040 → 00:23:51,640]** Yeah, because the whole thing that they are working on,

**[00:23:51,640 → 00:23:54,360]** for example, this is from an app team,

**[00:23:54,360 → 00:23:57,880]** they will send a message to the database.

**[00:23:57,880 → 00:24:00,760]** And then you just make sure that everyone has a key--

### 24:00

**[00:24:00,760 → 00:24:01,640]** [INTERPOSING VOICES]

**[00:24:01,640 → 00:24:04,200]** Yeah, has a key to retrieve the information.

**[00:24:04,200 → 00:24:07,240]** So for example, let's say, because actually it's a case,

**[00:24:07,240 → 00:24:10,920]** we have a team working on busking.

**[00:24:10,920 → 00:24:11,400]** Busking.

**[00:24:11,400 → 00:24:16,800]** So busking means they have a heat lamp, and then the lamp

**[00:24:16,800 → 00:24:17,800]** will actually--

**[00:24:17,800 → 00:24:19,160]** it's a ceramic heater.

**[00:24:19,160 → 00:24:20,760]** It will generate the heat.

**[00:24:20,760 → 00:24:23,240]** And then they have some areas, which

**[00:24:23,240 → 00:24:26,760]** actually making use of some slits, because slits,

**[00:24:26,760 → 00:24:29,440]** it's actually a piece of stone.

**[00:24:29,440 → 00:24:32,880]** Stone material, so that it will absorb the heat.

**[00:24:32,880 → 00:24:34,320]** And then it will fill up the area.

**[00:24:34,320 → 00:24:37,960]** So now, for this one, maybe the data

**[00:24:37,960 → 00:24:40,400]** that is being captured will store here.

**[00:24:40,400 → 00:24:43,160]** So I will actually go on and then start

**[00:24:43,160 → 00:24:45,120]** talking about the protocol later on.

**[00:24:45,120 → 00:24:46,600]** But at least make sure that--

**[00:24:46,600 → 00:24:48,800]** like the workflow that I mentioned,

**[00:24:48,800 → 00:24:50,680]** the first thing is that understand

**[00:24:50,680 → 00:24:54,840]** the sensor, and the circuit, and the physical structure,

**[00:24:54,840 → 00:24:57,000]** because you need to create a physical object so that it

**[00:24:57,000 → 00:24:59,080]** can be mounted somewhere, right?

**[00:24:59,080 → 00:25:02,840]** And the next is interleasing, the somewhere.

### 25:00

**[00:25:02,840 → 00:25:03,960]** And then this one is the software.

**[00:25:03,960 → 00:25:05,400]** Software is relatively easy.

**[00:25:05,400 → 00:25:06,720]** Once you understand the hardware,

**[00:25:06,720 → 00:25:10,480]** then the mixing will be spent many times.

**[00:25:10,480 → 00:25:12,760]** Even using all these church ADP or whatever

**[00:25:12,760 → 00:25:15,920]** 〔待核〕 the AI will write a lot of protocols.

**[00:25:15,920 → 00:25:22,800]** But as a check team, we have to define a standard of data.

**[00:25:22,800 → 00:25:25,040]** Now, for example, we have to define a standard

**[00:25:25,040 → 00:25:27,840]** 〔待核〕 on protocols, right?

**[00:25:27,840 → 00:25:28,760]** Communication protocols.

**[00:25:28,760 → 00:25:32,880]** So I'm using WebSocket, using JSON.

**[00:25:32,880 → 00:25:34,600]** JSON is easy to use.

**[00:25:34,600 → 00:25:38,360]** So later on, I will define a protocol

**[00:25:38,360 → 00:25:39,880]** at least as a standard protocol.

**[00:25:39,880 → 00:25:42,440]** But it basically is that whenever a device

**[00:25:42,440 → 00:25:44,920]** connected to the system, there should

**[00:25:44,920 → 00:25:48,440]** be some way for me to know the identity of that object

**[00:25:48,440 → 00:25:49,520]** and the type.

**[00:25:49,520 → 00:25:53,640]** So that's basically maybe we are talking about a protocol

**[00:25:53,640 → 00:25:56,520]** where whenever a new device connected,

**[00:25:56,520 → 00:26:01,840]** it will send out a message for curing its capabilities.

### 26:00

**[00:26:01,840 → 00:26:04,520]** And then it will check whether or if you

**[00:26:04,520 → 00:26:07,040]** are type walk and ID walk.

**[00:26:07,040 → 00:26:11,720]** So in our case, maybe we have three thermal sensors.

**[00:26:11,720 → 00:26:14,480]** So each of the thermal sensors may have its own separate ID,

**[00:26:14,480 → 00:26:15,880]** but the type are the same.

**[00:26:15,880 → 00:26:18,720]** So once the data comes in, the data

**[00:26:18,720 → 00:26:25,760]** will be stored in, for example, time ID and also data format.

**[00:26:25,760 → 00:26:27,200]** Something like this, right?

**[00:26:27,200 → 00:26:30,800]** So now, as long as we have a standard like this,

**[00:26:30,800 → 00:26:33,120]** it's easier for other people to read the information.

**[00:26:33,120 → 00:26:36,600]** So I hope that maybe by week end or maybe a little bit later,

**[00:26:36,600 → 00:26:39,680]** we have the standard so that you can retrieve the information.

**[00:26:39,680 → 00:26:42,400]** So for example, maybe for your case,

**[00:26:42,400 → 00:26:46,040]** you also want to know some other information outside

**[00:26:46,040 → 00:26:47,560]** of the camera.

**[00:26:47,560 → 00:26:50,600]** But then it will help to facilitate use, right?

**[00:26:50,600 → 00:26:52,400]** So that's why what I want to explain

**[00:26:52,400 → 00:26:55,040]** is that from the user perspective,

**[00:26:55,040 → 00:26:57,800]** maybe they want to measure something.

**[00:26:57,800 → 00:27:01,200]** Like, for example, how often they get into a tunnel.

### 27:00

**[00:27:01,200 → 00:27:05,440]** That's something that is above the basic behavior

**[00:27:05,440 → 00:27:06,360]** of the whole system.

**[00:27:06,360 → 00:27:09,280]** But then if you can do it, then you can actually

**[00:27:09,280 → 00:27:10,480]** put it into the requirement.

**[00:27:10,480 → 00:27:13,600]** That's what's assigned to it.

**[00:27:13,600 → 00:27:18,160]** So basically, we also need to know the habit of a gecko

**[00:27:18,160 → 00:27:23,440]** and to see what are the valuable information that we can--

**[00:27:23,440 → 00:27:25,720]** yeah, yeah, actually, I can provide more

**[00:27:25,720 → 00:27:29,680]** because I have experience with working with the students

**[00:27:29,680 → 00:27:30,440]** last time I said.

**[00:27:30,440 → 00:27:33,120]** Also, there is a report from last year's students.

**[00:27:33,120 → 00:27:35,080]** You can also have a look.

**[00:27:35,080 → 00:27:36,840]** They're doing the same thing, right?

**[00:27:36,840 → 00:27:37,640]** No, not exactly.

**[00:27:37,640 → 00:27:40,120]** Last year at the tunnel, they are not doing that.

**[00:27:40,120 → 00:27:41,560]** Because last year, we didn't have time

**[00:27:41,560 → 00:27:43,720]** to create the IoT system.

**[00:27:43,720 → 00:27:45,280]** So maybe I can show the--

**[00:27:45,280 → 00:27:47,920]** [INTERPOSING VOICES]

**[00:27:47,920 → 00:27:51,160]** Check it again.

**[00:27:51,160 → 00:27:56,440]** So I think it's in this page.

**[00:27:56,440 → 00:28:01,320]** So here is a final report.

### 28:00

**[00:28:01,320 → 00:28:20,080]** So what they were doing last year

**[00:28:20,080 → 00:28:24,400]** is to explore tunnels.

**[00:28:24,400 → 00:28:28,000]** So it was done by students in the MC program.

**[00:28:28,000 → 00:28:31,120]** So what they were doing is that they

**[00:28:31,120 → 00:28:36,120]** have some background material about gecko's behavior.

**[00:28:36,120 → 00:28:43,480]** And also, they actually built the whole thing.

**[00:28:43,480 → 00:28:47,200]** And then they changed the tunnel structure

**[00:28:47,200 → 00:28:50,480]** to see what type of tunnel structure

**[00:28:50,480 → 00:28:52,720]** would be preferred to them.

**[00:28:52,720 → 00:28:54,760]** Like, for example, the dimension,

**[00:28:54,760 → 00:28:57,520]** where the tunnel should be placed, and also--

**[00:28:57,520 → 00:29:00,680]** for example, I remember they actually found that--

### 29:00

**[00:29:00,680 → 00:29:03,440]** for example, this tunnel was too small.

**[00:29:03,440 → 00:29:05,120]** This one is bigger tunnel.

**[00:29:05,120 → 00:29:07,560]** So they actually not climb inside the tunnel,

**[00:29:07,560 → 00:29:09,760]** but actually climb on top of the tunnel.

**[00:29:09,760 → 00:29:12,600]** And also, this kind of tunnel is too slippery.

**[00:29:12,600 → 00:29:15,600]** Because the gecko that we are using is called leopard gecko.

**[00:29:15,600 → 00:29:18,440]** The leopard gecko has claws.

**[00:29:18,440 → 00:29:20,320]** They cannot stick onto the wall.

**[00:29:20,320 → 00:29:23,760]** So that's why this kind of tunnel is not working.

**[00:29:23,760 → 00:29:24,360]** We found that.

**[00:29:24,360 → 00:29:26,760]** It's actually-- afterwards, we tried that.

**[00:29:26,760 → 00:29:30,440]** So they also tried some unstable platform.

**[00:29:30,440 → 00:29:38,200]** Like, for example, this kind of tunnel,

**[00:29:38,200 → 00:29:43,880]** where they hang a lamp, so that it's more like a swing.

**[00:29:43,880 → 00:29:48,680]** So they have to-- it's a little bit not secure.

**[00:29:48,680 → 00:29:52,200]** And it seems like they do not like to walk in this unsecured

**[00:29:52,200 → 00:29:53,000]** space.

**[00:29:53,000 → 00:29:55,840]** So that's what we did last time, last year.

**[00:29:55,840 → 00:30:00,080]** And then, originally, I wanted to create a more like a LEGO

### 30:00

**[00:30:00,080 → 00:30:03,160]** system, where they can connect easily,

**[00:30:03,160 → 00:30:05,000]** or reconnect easily the tunnels.

**[00:30:05,000 → 00:30:07,200]** But then they did not have time.

**[00:30:07,200 → 00:30:09,880]** But they just based on the existing product.

**[00:30:09,880 → 00:30:12,280]** And then they fly by the product and change.

**[00:30:12,280 → 00:30:15,720]** And then see the behavior changes of the gecko.

**[00:30:15,720 → 00:30:17,720]** But the big problem is that we do not

**[00:30:17,720 → 00:30:23,080]** have ways to, how to say, capture the actual activity

**[00:30:23,080 → 00:30:24,920]** information of the gecko.

**[00:30:24,920 → 00:30:28,760]** So actually, if we were going to repeat the whole thing,

**[00:30:28,760 → 00:30:32,040]** we can actually set up a new tunnel system.

**[00:30:32,040 → 00:30:34,720]** And then, if we have a way to measure

**[00:30:34,720 → 00:30:37,080]** the activity of the gecko, we can

**[00:30:37,080 → 00:30:42,480]** worry by, because of the changes in the configuration, whether

**[00:30:42,480 → 00:30:44,920]** there will be increases in activity.

**[00:30:44,920 → 00:30:46,680]** So that's right now, at that time,

**[00:30:46,680 → 00:30:49,040]** yes, last year, we have difficulty in doing that,

**[00:30:49,040 → 00:30:51,680]** because it takes a lot of time to analyze the data.

**[00:30:51,680 → 00:30:53,840]** That's why-- what you do is that maybe we

**[00:30:53,840 → 00:30:57,880]** can have some way to analyze the capture data.

**[00:30:57,880 → 00:31:00,520]** I'm wondering, the ns presence should be automatically

### 31:00

**[00:31:00,520 → 00:31:02,120]** 〔待核〕 all manually, because--

**[00:31:02,120 → 00:31:05,400]** I'm expecting manual together with automatic.

**[00:31:05,400 → 00:31:07,440]** It doesn't account automatically everything.

**[00:31:07,440 → 00:31:11,640]** So we don't need to apply some, like, a recognition

**[00:31:11,640 → 00:31:12,680]** 〔待核〕 AI model into this?

**[00:31:12,680 → 00:31:13,200]** Yeah.

**[00:31:13,200 → 00:31:13,680]** Maybe.

**[00:31:13,680 → 00:31:14,240]** It depends.

**[00:31:14,240 → 00:31:14,680]** It depends.

**[00:31:14,680 → 00:31:15,160]** OK.

**[00:31:15,160 → 00:31:19,040]** Now, actually, one more thing is that, as I mentioned here,

**[00:31:19,040 → 00:31:22,280]** is that it's about the well-being of the gecko.

**[00:31:22,280 → 00:31:25,760]** Because for gecko, we also want to measure--

**[00:31:25,760 → 00:31:29,720]** we also want to know whether the behavior of the gecko

**[00:31:29,720 → 00:31:33,240]** is having some strange behavior.

**[00:31:33,240 → 00:31:38,120]** The thing is, I think I mentioned about this one.

**[00:31:38,120 → 00:31:40,240]** Like, for example, this one, we want

**[00:31:40,240 → 00:31:43,000]** to know whether the gecko has some strange behavior.

**[00:31:43,000 → 00:31:44,480]** This is strange behavior.

**[00:31:44,480 → 00:31:47,440]** It's not normal, because it's interact with a transparent

**[00:31:47,440 → 00:31:48,360]** barrier.

**[00:31:48,360 → 00:31:51,160]** So now, I guess maybe for the gecko,

**[00:31:51,160 → 00:31:53,240]** we may also have some strange behavior,

**[00:31:53,240 → 00:31:56,040]** not just about hitting onto the wall,

**[00:31:56,040 → 00:31:59,640]** but also maybe they will hide, or maybe they

**[00:31:59,640 → 00:32:02,560]** will stay in a particular place for too long.

### 32:00

**[00:32:02,560 → 00:32:05,680]** Actually, if they are staying in a particular place

**[00:32:05,680 → 00:32:07,920]** inside an environment for too long,

**[00:32:07,920 → 00:32:09,480]** it means some problem.

**[00:32:09,480 → 00:32:13,280]** So supposedly, if you have some AI or recommendation system,

**[00:32:13,280 → 00:32:16,160]** you can process the information, you can actually recognize.

**[00:32:16,160 → 00:32:17,440]** And then you can recommend.

**[00:32:17,440 → 00:32:19,520]** So that's why what I mentioned here

**[00:32:19,520 → 00:32:24,240]** is that facilitate their care.

**[00:32:24,240 → 00:32:26,120]** That's care.

**[00:32:26,120 → 00:32:29,720]** So that's why it's not just engineering problem.

**[00:32:29,720 → 00:32:32,520]** So now, if you want to know more about the behavior

**[00:32:32,520 → 00:32:36,240]** 〔待核〕 that's moving the scene, I'll answer that more.

**[00:32:36,240 → 00:32:40,600]** Yeah, let me ask a question, because I might think a bit

**[00:32:40,600 → 00:32:45,200]** far, because let's say I got a personal idea.

**[00:32:45,200 → 00:32:48,880]** It is from some experiment from your phone.

**[00:32:48,880 → 00:32:52,360]** So if you want to see the GitHub,

**[00:32:52,360 → 00:32:56,640]** there are a type of experiment when the AI--

**[00:32:56,640 → 00:32:59,640]** when some sort of program automatically

**[00:32:59,640 → 00:33:03,280]** capturing your screen during the daily use.

### 33:00

**[00:33:03,280 → 00:33:09,520]** And then you can use that kind of screenshots or videos,

**[00:33:09,520 → 00:33:15,000]** and you upload it to an API, AI, API, chat GPT, et cetera.

**[00:33:15,000 → 00:33:19,560]** And then the chat GPT will analyze your daily routines.

**[00:33:19,560 → 00:33:22,080]** And it might know you better, and it

**[00:33:22,080 → 00:33:25,680]** might give you some answers that you're not expected.

**[00:33:25,680 → 00:33:30,400]** I think that's the kind of way it is much more suitable

**[00:33:30,400 → 00:33:32,720]** for monitoring a get-go.

**[00:33:32,720 → 00:33:39,000]** But the hardest point is that the API, the AI, it costs a lot.

**[00:33:39,000 → 00:33:41,760]** So also, we are training the AI model.

**[00:33:41,760 → 00:33:42,800]** It also costs a lot.

**[00:33:42,800 → 00:33:45,080]** So that's why right now, we are not

**[00:33:45,080 → 00:33:48,360]** expecting to use various sophisticated AI models.

**[00:33:48,360 → 00:33:50,560]** And also, we are still in the early stage.

**[00:33:50,560 → 00:33:54,720]** We are just making sure that data are being collected.

**[00:33:54,720 → 00:33:55,720]** 〔待核〕 Yeah.

**[00:33:55,720 → 00:33:58,320]** Yeah, that's what you're talking about is the next phase.

**[00:33:58,320 → 00:34:00,280]** Oh, and the next phase.

### 34:00

**[00:34:00,280 → 00:34:02,480]** Maybe if you have time, you can actually work on the next phase.

**[00:34:02,480 → 00:34:03,480]** Yeah.

**[00:34:03,480 → 00:34:06,560]** 〔待核〕 Yeah, you can try and create our own recognition model.

**[00:34:06,560 → 00:34:08,880]** I can boil you down to the board.

**[00:34:08,880 → 00:34:11,200]** Actually, from my personal experience,

**[00:34:11,200 → 00:34:14,360]** I don't think it's-- well, you don't need money, actually.

**[00:34:14,360 → 00:34:16,960]** Actually, the reason why we have to produce those models

**[00:34:16,960 → 00:34:20,800]** is because those models has a lot more sophisticated behavior.

**[00:34:20,800 → 00:34:23,240]** But actually, when we are talking about simple things,

**[00:34:23,240 → 00:34:27,120]** like, for example, the frequency of the--

**[00:34:27,120 → 00:34:28,080]** OK, OK, OK.

**[00:34:28,080 → 00:34:28,880]** 〔待核〕 It's simple.

**[00:34:28,880 → 00:34:29,480]** Yeah, I got it.

**[00:34:29,480 → 00:34:30,600]** You just use OpenCV.

**[00:34:30,600 → 00:34:31,400]** Yeah, yeah, yeah.

**[00:34:31,400 → 00:34:33,880]** Actually, it's not OpenCV because we can use--

**[00:34:33,880 → 00:34:36,600]** 〔待核〕 because the chat that's for Rock5,

**[00:34:36,600 → 00:34:40,000]** it has more like a GPU.

**[00:34:40,000 → 00:34:41,040]** It can do image processing.

**[00:34:41,040 → 00:34:41,720]** Oh, OK.

**[00:34:41,720 → 00:34:43,800]** So we can do it by ourselves.

**[00:34:43,800 → 00:34:45,720]** So that's why we can actually look at it.

**[00:34:45,720 → 00:34:46,800]** Search for it.

**[00:34:46,800 → 00:34:52,920]** For Rock5, they have some examples of NBC,

**[00:34:52,920 → 00:34:56,960]** 〔待核〕 network video storage, and NDS, right?

**[00:34:56,960 → 00:34:57,440]** OK, OK, OK.

**[00:34:57,440 → 00:35:01,960]** So because these are very usual, frequently used application

### 35:00

**[00:35:01,960 → 00:35:03,560]** for these embedded systems.

**[00:35:03,560 → 00:35:06,360]** So what they are doing is they connect--

**[00:35:06,360 → 00:35:10,560]** they mentioned that I think you can feed five video streams

**[00:35:10,560 → 00:35:12,720]** into a Rock5.

**[00:35:12,720 → 00:35:13,760]** They mentioned that.

**[00:35:13,760 → 00:35:16,760]** And then you can do real-time image segmentation

**[00:35:16,760 → 00:35:18,080]** and image retention.

**[00:35:18,080 → 00:35:18,680]** Oh, OK.

**[00:35:18,680 → 00:35:19,720]** So that can be done, OK?

**[00:35:19,720 → 00:35:20,560]** Yeah, yeah, OK.

**[00:35:20,560 → 00:35:21,960]** So that's not complex.

**[00:35:21,960 → 00:35:24,040]** You don't need to use an AI model.

**[00:35:24,040 → 00:35:25,840]** The reason why you use an AI model

**[00:35:25,840 → 00:35:28,680]** is because, for example, you want

**[00:35:28,680 → 00:35:31,960]** to be able to recognize language.

**[00:35:31,960 → 00:35:32,800]** Yeah, yeah.

**[00:35:32,800 → 00:35:35,280]** So that's complex.

**[00:35:35,280 → 00:35:38,880]** 〔待核〕 But we are not going to [INAUDIBLE]

**[00:35:38,880 → 00:35:41,560]** Frankly, we are going to learn--

**[00:35:41,560 → 00:35:43,640]** we are going to capture data.

**[00:35:43,640 → 00:35:48,000]** It's good enough already if we are using those machine learning

**[00:35:48,000 → 00:35:48,560]** algorithms.

**[00:35:48,560 → 00:35:49,360]** Yeah, OK, yeah.

**[00:35:49,360 → 00:35:52,800]** For example, you can use, for example, TensorFlow.

**[00:35:52,800 → 00:35:55,880]** You don't have to use the latest LRM.

**[00:35:55,880 → 00:35:56,520]** Yes, yes.

**[00:35:56,520 → 00:35:58,840]** [INTERPOSING VOICES]

**[00:35:58,840 → 00:36:00,200]** I know that technology is useful,

### 36:00

**[00:36:00,200 → 00:36:02,840]** but it's actually not that useful here, right?

**[00:36:02,840 → 00:36:08,960]** So that's why if we can capture as simple as occurrence

**[00:36:08,960 → 00:36:14,040]** frequency, for example, like, for example, this one, right?

**[00:36:14,040 → 00:36:17,120]** This one actually came from the camera.

**[00:36:17,120 → 00:36:18,360]** Because we have the background.

**[00:36:18,360 → 00:36:20,880]** We can use image difference there.

**[00:36:20,880 → 00:36:22,760]** Extract the foreground information,

**[00:36:22,760 → 00:36:26,480]** and then identify by counting pixels.

**[00:36:26,480 → 00:36:29,720]** And then we can-- well, that's standard surveillance thing.

**[00:36:29,720 → 00:36:31,600]** And then we can know there are some activities.

**[00:36:31,600 → 00:36:35,240]** And then based on the activity, then we extract the frame,

**[00:36:35,240 → 00:36:37,160]** and then do the pattern recognition.

**[00:36:37,160 → 00:36:38,360]** That's what I mentioned to her.

**[00:36:38,360 → 00:36:42,440]** I will tell you, you can actually recognize the gecko,

**[00:36:42,440 → 00:36:43,840]** but look at the patterns.

**[00:36:43,840 → 00:36:45,960]** Because the patterns are unique.

**[00:36:45,960 → 00:36:47,920]** But of course, the pattern is evolving.

**[00:36:47,920 → 00:36:50,080]** Now, for recognizing patterns, you

**[00:36:50,080 → 00:36:54,120]** can use teachable AI, teachable machines,

**[00:36:54,120 → 00:36:58,160]** or maybe some other simple classifier.

**[00:36:58,160 → 00:37:00,160]** You don't have to use LRM, frankly.

### 37:00

**[00:37:00,160 → 00:37:05,000]** So that's why-- well, because my PhD wasn't AI,

**[00:37:05,000 → 00:37:05,840]** 〔待核〕 you were an equity.

**[00:37:05,840 → 00:37:08,880]** So that's why if you are thinking about this as a classifier

**[00:37:08,880 → 00:37:10,480]** problem, it's easier.

**[00:37:10,480 → 00:37:14,240]** So you can use traditional pattern recognition model.

**[00:37:14,240 → 00:37:17,240]** You can recognize the image, and then feed it to learn.

**[00:37:17,240 → 00:37:20,520]** And we don't have to train our--

**[00:37:20,520 → 00:37:22,480]** 〔待核〕 yeah, the model has a free--

**[00:37:22,480 → 00:37:23,280]** I think so.

**[00:37:23,280 → 00:37:24,000]** No, no, no.

**[00:37:24,000 → 00:37:25,560]** 〔待核〕 So you don't have to do this.

**[00:37:25,560 → 00:37:27,240]** You have to capture data.

**[00:37:27,240 → 00:37:30,000]** Now, suppose that we run this one,

**[00:37:30,000 → 00:37:32,360]** and then run for maybe one month.

**[00:37:32,360 → 00:37:36,120]** Then we can actually capture the real texture

**[00:37:36,120 → 00:37:37,320]** information of the gecko.

**[00:37:37,320 → 00:37:40,000]** And then we can feed it to the training model.

**[00:37:40,000 → 00:37:40,880]** That's actually doable.

**[00:37:40,880 → 00:37:43,040]** Because this one is actually-- it makes a difference.

**[00:37:43,040 → 00:37:46,560]** 〔待核〕 Because when you do data frame, you're over that.

**[00:37:46,560 → 00:37:47,160]** Yeah, yeah.

**[00:37:47,160 → 00:37:47,660]** 〔待核〕 Sure.

**[00:37:47,660 → 00:37:49,600]** So for these neural networks, you can use TensorFlow.

**[00:37:49,600 → 00:37:51,760]** You don't have to use expensive LL.

**[00:37:51,760 → 00:37:52,760]** I'm sorry.

**[00:37:52,760 → 00:37:54,560]** The model I'm talking about is a neuron.

**[00:37:54,560 → 00:37:55,560]** It's not LL.

**[00:37:55,560 → 00:37:56,800]** Yeah, yeah, yeah.

## 片尾边界说明

完整音轨已处理，但语音模型可能把片尾时间估到文件之外，也可能不为末尾短暂停顿输出文字；这不是录像外存在额外发言的证据。原始时间戳保留以便追溯。
