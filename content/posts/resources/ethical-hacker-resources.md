+++
aliases = ["/posts/ethical-hacker-resources/"]
category = "technology"
comments = true
date = "2020-06-10"
description = "In which Alex supplies a master list of his notes on ethical hacking."
dropcap = false
tags = ["security"]
title = "Ethical Hacker Resources"
[featuredImage]
  alt = "Graham Hacks on Computer"
  large = "https://3urseq.by.files.1drv.com/y4mdiDQgm-HdM-cjE8mAIdkdajVAZLj-CCDr-fqcj_MNL5_kM-tr-rc6IApxigB4n5APgeg-dMWhjuPi-VmO1t3xg3L8nPgqcap7yxAK3eaOgfk7lHZZq29_vvpiRvaU6pV16yFq4xhhwenedjYd_6F2Rn_txqj0Xpjjf6Ij4kiERDvsR6NJ7XE0T1eRGnxNVd7GLAaD108zMD28g2ZyeJGWg?width=768&height=1024&cropmode=none"
  small = "https://3urseq.by.files.1drv.com/y4mdiDQgm-HdM-cjE8mAIdkdajVAZLj-CCDr-fqcj_MNL5_kM-tr-rc6IApxigB4n5APgeg-dMWhjuPi-VmO1t3xg3L8nPgqcap7yxAK3eaOgfk7lHZZq29_vvpiRvaU6pV16yFq4xhhwenedjYd_6F2Rn_txqj0Xpjjf6Ij4kiERDvsR6NJ7XE0T1eRGnxNVd7GLAaD108zMD28g2ZyeJGWg?width=192&height=256&cropmode=none"
+++

These notes were taken while watching the [PluralSight](https://app.pluralsight.com/paths/certificate/ethical-hacking-ceh-prep-2018) courses for the Certified Ethical Hacking (CEH) curriculum. They are not comprehensive so, if the content interests you, I highly recommend watching the videos for yourself.

To purchase the official study guide, visit [this site](https://www.wiley.com/en-us/CEH+v10+Certified+Ethical+Hacker+Study+Guide-p-9781119533269). However, the [Hacker Playbook v2](https://www.amazon.com/dp/1512214566/ref=as_li_ss_tl?cv_ct_id=amzn1.idea.2A2G5RW8E6Q5J&cv_ct_pg=storefront&cv_ct_wn=aip-storefront&ref=exp_cov_ceos3ctutorials_dp_vv_d&linkCode=sl1&tag=ceos3c666-20&linkId=4c0880aebec44c0491e56e051c3c2b9e&language=en_US) and [Ghost in the Wires](https://www.amazon.com/dp/0316037729/ref=as_li_ss_tl?cv_ct_id=amzn1.idea.2A2G5RW8E6Q5J&cv_ct_pg=storefront&cv_ct_wn=aip-storefront&ref=exp_cov_ceos3ctutorials_dp_vv_d&linkCode=sl1&tag=ceos3c666-20&linkId=46fc9f7057949d83035b9a21507307b5&language=en_US) may be more suitable for practice and excitement. The official study guide looks overly verbose and lacks practical examples. If I want to delve deeper before going to the study guide, the [Hacker Playbook v3](https://www.amazon.com/Hacker-Playbook-Practical-Penetration-Testing-ebook/dp/B07CSPFYZ2/ref=pd_sim_ebk_14_2/146-7743441-1390659?_encoding=UTF8&pd_rd_i=B07CSPFYZ2&pd_rd_r=f94b34df-328d-4499-810f-8e5981851c7c&pd_rd_w=nPlYC&pd_rd_wg=kkCmH&pf_rd_p=dc5f8131-4953-4e94-b701-14887e2f8999&pf_rd_r=ZN8PNSC5N04M3JXJV0WN&psc=1&refRID=ZN8PNSC5N04M3JXJV0WN) may be a better option (content is more advanced than v2) or even the seminal tome, [Hacking, The Art of Exploitation](https://www.amazon.com/Hacking-Art-Exploitation-Jon-Erickson-ebook/dp/B004OEJN3I/ref=pd_sim_ebk_14_5/146-7743441-1390659?_encoding=UTF8&pd_rd_i=B004OEJN3I&pd_rd_r=f94b34df-328d-4499-810f-8e5981851c7c&pd_rd_w=nPlYC&pd_rd_wg=kkCmH&pf_rd_p=dc5f8131-4953-4e94-b701-14887e2f8999&pf_rd_r=ZN8PNSC5N04M3JXJV0WN&psc=1&refRID=ZN8PNSC5N04M3JXJV0WN).

Below are links to posts with content specific to an ethical hacking subject.

{{< backref src="/posts/resources/reconnaissance" >}} also referred to as footprinting, is the first step a hacker takes in their path to hacking your system.

{{< backref src="/posts/resources/scanning" >}} is the next step after reconnaissance. While reconnaissance is silent and does not require any direct connection to the target network, scanning does access the target network.

Enumeration, is a hacker's methodical data gathering from individual machines that make up the target network. While scanning should begin a netowrk map, enumeration fills it out with user accounts, machine names, OSes, and more.

Denial of Service (DoS) floods a network service with requests to overload the target system and ensure other's can't receive the service. One machine is rarely sufficient, so DoS attacks are almost always distributed (DDoS).

Social Engineering is the art of manipulating humans to act abnormally in order to gain access to their networks. For a practical example, see my post about {{< backref src="/posts/insights/police-impersonation-scam" >}}.

{{< backref src="/posts/resources/session-hijacking" >}} happens when a hacker steals identifying information from a user's session to access their data, impersonate them, or hinder their access.
