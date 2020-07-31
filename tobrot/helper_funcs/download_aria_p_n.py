#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import aria2p
import asyncio
import os
from tobrot.helper_funcs.upload_to_tg import upload_to_tg, upload_to_gdrive
from tobrot.helper_funcs.create_compressed_archive import create_archive, unzip_me, unrar_me, untar_me
from tobrot.helper_funcs.extract_link_from_message import extract_link

from tobrot import (
    ARIA_TWO_STARTED_PORT,
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START,
    AUTH_CHANNEL,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    CUSTOM_FILE_NAME
)
from pyrogram import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	Message
)

async def aria_start():
    aria2_daemon_start_cmd = []
    # start the daemon, aria2c command
    aria2_daemon_start_cmd.append("aria2c")
    # aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    # aria2_daemon_start_cmd.append(f"--dir={DOWNLOAD_LOCATION}")
    # TODO: this does not work, need to investigate this.
    # but for now, https://t.me/TrollVoiceBot?start=858
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--follow-torrent=mem")
    aria2_daemon_start_cmd.append("--max-connection-per-server=16")
    aria2_daemon_start_cmd.append("--min-split-size=4M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=false")
    aria2_daemon_start_cmd.append(f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append("--seed-ratio=1")
    aria2_daemon_start_cmd.append("--seed-time=0.01")
    aria2_daemon_start_cmd.append("--split=10")
    aria2_daemon_start_cmd.append("--bt-tracker-timeout=10")
    aria2_daemon_start_cmd.append("--bt-tracker-connect-timeout=10")
    aria2_daemon_start_cmd.append("--enable-dht=true")
    aria2_daemon_start_cmd.append("--peer-id-prefix=-TR2770-")
    aria2_daemon_start_cmd.append("--user-agent=Transmission/2.77")
    aria2_daemon_start_cmd.append("--bt-tracker=http://00.mercax.com:443/announce,http://0205.uptm.ch:6969/announce,http://104.238.198.186:8000/announce,http://1337.abcvg.info:80/announce,http://178.175.143.27:80/announce,http://78.30.254.12:2710/announce,http://91.217.91.21:3218/announce,http://93.92.64.5:80/announce,http://[2001:1b10:1000:8101:0:242:ac11:2]:6969/announce,http://[2001:470:1:189:0:1:2:3]:6969/announce,http://[2a04:ac00:1:3dd8::1:2710]:2710/announce,http://aaa.army:8866/announce,http://atrack.pow7.com:80/announce,http://bobbialbano.com:6969/announce,http://bt.pusacg.org:8080/announce,http://dn42.smrsh.net:6969/announce,http://explodie.org:6969/announce,http://grifon.info:80/announce,http://h4.trakx.nibba.trade:80/announce,http://ns3107607.ip-54-36-126.eu:6969/announce,http://ns349743.ip-91-121-106.eu:80/announce,http://open.acgnxtracker.com:80/announce,http://open.acgtracker.com:1096/announce,http://open.touki.ru:80/announce.php,http://opentracker.i2p.rocks:6969/announce,http://pow7.com:80/announce,http://retracker.hotplug.ru:2710/announce,http://retracker.krs-ix.ru:80/announce,http://retracker.sevstar.net:2710/announce,http://retracker.spark-rostov.ru:80/announce,http://rt.tace.ru:80/announce,http://secure.pow7.com:80/announce,http://share.camoe.cn:8080/announce,http://t.acg.rip:6699/announce,http://t.nyaatracker.com:80/announce,http://t.overflow.biz:6969/announce,http://t1.pow7.com:80/announce,http://t2.pow7.com:80/announce,http://thetracker.org:80/announce,http://torrent.nwps.ws:80/announce,http://torrentsmd.com:8080/announce,http://torrenttracker.nwc.acsalaska.net:6969/announce,http://tr.cili001.com:8070/announce,http://tr.kxmp.cf:80/announce,http://tracker.anonwebz.xyz:8080/announce,http://tracker.birkenwald.de:6969/announce,http://tracker.bittor.pw:1337/announce,http://tracker.bt4g.com:2095/announce,http://tracker.bz:80/announce,http://tracker.dler.org:6969/announce,http://tracker.dutchtracking.nl:80/announce,http://tracker.files.fm:6969/announce,http://tracker.gbitt.info:80/announce,http://tracker.ipv6tracker.ru:80/announce,http://tracker.kuroy.me:5944/announce,http://tracker.lelux.fi:80/announce,http://tracker.moeking.me:6969/announce,http://tracker.nyap2p.com:8080/announce,http://tracker.opentrackr.org:1337/announce,http://tracker.publicbt.com:80/announce,http://tracker.sloppyta.co:80/announce,http://tracker.trackerfix.com:80/announce,http://tracker.tyker.xyz:8080/announce,http://tracker.uw0.xyz:6969/announce,http://tracker.ygsub.com:6969/announce,http://tracker.yoshi210.com:6969/announce,http://tracker.zerobytes.xyz:1337/announce,http://tracker.zum.bi:6969/announce,http://tracker1.itzmx.com:8080/announce,http://tracker2.dler.org:80/announce,http://tracker2.itzmx.com:6961/announce,http://tracker3.itzmx.com:6961/announce,http://trun.tom.ru:80/announce,http://vpn.flying-datacenter.de:6969/announce,http://vps02.net.orel.ru:80/announce,http://www.wareztorrent.com:80/announce,https://1337.abcvg.info:443/announce,https://2.tracker.eu.org:443/announce,https://3.tracker.eu.org:443/announce,https://aaa.army:8866/announce,https://opentracker.acgnx.se:443/announce,https://tr.ready4.icu:443/announce,https://tracker.bt-hash.com:443/announce,https://tracker.gbitt.info:443/announce,https://tracker.hama3.net:443/announce,https://tracker.imgoingto.icu:443/announce,https://tracker.jae.moe:443/announce,https://tracker.lelux.fi:443/announce,https://tracker.nitrix.me:443/announce,https://tracker.skynetcloud.site:8443/announce,https://tracker.sloppyta.co:443/announce,https://tracker.tamersunion.org:443/announce,https://tracker6.lelux.fi:443/announce,https://trakx.herokuapp.com:443/announce,https://w.wwwww.wtf:443/announce,udp://104.238.198.186:8000/announce,udp://107.150.14.110:6969/announce,udp://109.121.134.121:1337/announce,udp://114.55.113.60:6969/announce,udp://128.199.70.66:5944/announce,udp://151.80.120.114:2710/announce,udp://168.235.67.63:6969/announce,udp://178.33.73.26:2710/announce,udp://182.176.139.129:6969/announce,udp://185.5.97.139:8089/announce,udp://185.83.215.123:6969/announce,udp://185.86.149.205:1337/announce,udp://188.165.253.109:1337/announce,udp://191.101.229.236:1337/announce,udp://194.106.216.222:80/announce,udp://195.123.209.37:1337/announce,udp://195.123.209.40:80/announce,udp://208.67.16.113:8000/announce,udp://212.1.226.176:2710/announce,udp://212.47.227.58:6969/announce,udp://213.163.67.56:1337/announce,udp://37.19.5.155:2710/announce,udp://46.4.109.148:6969/announce,udp://47.ip-51-68-199.eu:6969/announce,udp://5.79.249.77:6969/announce,udp://5.79.83.193:6969/announce,udp://51.254.244.161:6969/announce,udp://52.58.128.163:6969/announce,udp://61626c.net:6969/announce,udp://62.138.0.158:6969/announce,udp://62.212.85.66:2710/announce,udp://6ahddutb1ucc3cp.ru:6969/announce,udp://74.82.52.209:6969/announce,udp://78.30.254.12:2710/announce,udp://85.17.19.180:80/announce,udp://89.234.156.205:80/announce,udp://9.rarbg.com:2710/announce,udp://9.rarbg.me:2710/announce,udp://9.rarbg.me:2780/announce,udp://9.rarbg.to:2710/announce,udp://9.rarbg.to:2730/announce,udp://91.216.110.52:451/announce,udp://91.218.230.81:6969/announce,udp://94.23.183.33:6969/announce,udp://95.211.168.204:2710/announce,udp://[2001:1b10:1000:8101:0:242:ac11:2]:6969/announce,udp://[2001:470:1:189:0:1:2:3]:6969/announce,udp://[2a03:7220:8083:cd00::1]:451/announce,udp://[2a04:ac00:1:3dd8::1:2710]:2710/announce,udp://[2a04:c44:e00:32e0:4cf:6aff:fe00:aa1]:6969/announce,udp://aaa.army:8866/announce,udp://admin.videoenpoche.info:6969/announce,udp://adminion.n-blade.ru:6969/announce,udp://api.bitumconference.ru:6969/announce,udp://aruacfilmes.com.br:6969/announce,udp://benouworldtrip.fr:6969/announce,udp://blokas.io:6969/announce,udp://bms-hosxp.com:6969/announce,udp://bt1.archive.org:6969/announce,udp://bt2.54new.com:8080/announce,udp://bt2.archive.org:6969/announce,udp://bubu.mapfactor.com:6969/announce,udp://cdn-1.gamecoast.org:6969/announce,udp://cdn-2.gamecoast.org:6969/announce,udp://chanchan.uchuu.co.uk:6969/announce,udp://chihaya.toss.li:9696/announce,udp://code2chicken.nl:6969/announce,udp://contra.sf.ca.us:6969/announce,udp://cpc69306-dudl11-0-0-cust33.16-1.cable.virginm.net:6969/announce,udp://cutiegirl.ru:6969/announce,udp://daveking.com:6969/announce,udp://discord.heihachi.pw:6969/announce,udp://dns.cctvqueretaro.com:53/announce,udp://dpiui.reedlan.com:6969/announce,udp://drumkitx.com:6969/announce,udp://eddie4.nl:6969/announce,udp://edenbridge.org.uk:6969/announce,udp://edu.uifr.ru:6969/announce,udp://eliastre100.fr:6969/announce,udp://engplus.ru:6969/announce,udp://exodus.desync.com:6969/announce,udp://exponage-api.com:6969/announce,udp://fe.dealclub.de:6969/announce,udp://forever-tracker.zooki.xyz:6969/announce,udp://forever.publictracker.xyz:6969/announce,udp://free-tracker.zooki.xyz:6969/announce,udp://git.vulnix.sh:6969/announce,udp://gra1.joshkeegan.co.uk:6969/announce,udp://handrew.me:6969/announce,udp://inferno.demonoid.is:3391/announce,udp://ipv4.tracker.harry.lu:80/announce,udp://ipv6.tracker.zerobytes.xyz:16661/announce,udp://josueunhuit.com:6969/announce,udp://kanal-4.de:6969/announce,udp://kanbooru.com:6969/announce,udp://kawaii.social:6969/announce,udp://koli.services:6969/announce,udp://line-net.ru:6969/announce,udp://ln.mtahost.co:6969/announce,udp://mail.realliferpg.de:6969/announce,udp://mgtracker.org:2710/announce,udp://movies.zsw.ca:6969/announce,udp://mts.tvbit.co:6969/announce,udp://nagios.tks.sumy.ua:80/announce,udp://open.demonii.com:1337/announce,udp://open.stealth.si:80/announce,udp://opentor.org:2710/announce,udp://opentracker.i2p.rocks:6969/announce,udp://peerfect.org:6969/announce,udp://public-tracker.zooki.xyz:6969/announce,udp://public.popcorn-tracker.org:6969/announce,udp://public.publictracker.xyz:6969/announce,udp://publictracker.xyz:6969/announce,udp://retracker.akado-ural.ru:80/announce,udp://retracker.hotplug.ru:2710/announce,udp://retracker.lanta-net.ru:2710/announce,udp://retracker.local.msn-net.ru:6969/announce,udp://retracker.netbynet.ru:2710/announce,udp://retracker.nts.su:2710/announce,udp://retracker.sevstar.net:2710/announce,udp://rutorrent.frontline-mod.com:6969/announce,udp://sd-161673.dedibox.fr:6969/announce,udp://shadowshq.eddie4.nl:6969/announce,udp://shadowshq.yi.org:6969/announce,udp://storage.groupees.com:6969/announce,udp://t1.leech.ie:1337/announce,udp://t2.leech.ie:1337/announce,udp://t3.leech.ie:1337/announce,udp://teamspeak.value-wolf.org:6969/announce,udp://thetracker.org:80/announce,udp://threads.run:6969/announce,udp://tr.bangumi.moe:6969/announce,udp://tr.cili001.com:8070/announce,udp://tr2.ysagin.top:2710/announce,udp://tracker-udp.gbitt.info:80/announce,udp://tracker-v6.zooki.xyz:6969/announce,udp://tracker.0o.is:6969/announce,udp://tracker.aletorrenty.pl:2710/announce,udp://tracker.archlinux.org.theoks.net:6969/announce,udp://tracker.army:6969/announce,udp://tracker.beeimg.com:6969/announce,udp://tracker.birkenwald.de:6969/announce,udp://tracker.bittor.pw:1337/announce,udp://tracker.blacksparrowmedia.net:6969/announce,udp://tracker.casual.run:6969/announce,udp://tracker.coppersurfer.tk:6969/announce,udp://tracker.cyberia.is:6969/announce,udp://tracker.dler.org:6969/announce,udp://tracker.ds.is:6969/announce,udp://tracker.dyne.org:6969/announce,udp://tracker.e-utp.net:6969/announce,udp://tracker.eddie4.nl:6969/announce,udp://tracker.ex.ua:80/announce,udp://tracker.filemail.com:6969/announce,udp://tracker.flashtorrents.org:6969/announce,udp://tracker.fortu.io:6969/announce,udp://tracker.gbitt.info:80/announce,udp://tracker.grepler.com:6969/announce,udp://tracker.halfchub.club:6969/announce,udp://tracker.iamhansen.xyz:2000/announce,udp://tracker.internetwarriors.net:1337/announce,udp://tracker.jae.moe:6969/announce,udp://tracker.kuroy.me:5944/announce,udp://tracker.leechers-paradise.org:6969/announce,udp://tracker.lelux.fi:6969/announce,udp://tracker.moeking.me:6969/announce,udp://tracker.open-internet.nl:6969/announce,udp://tracker.openbittorrent.com:80/announce,udp://tracker.opentrackr.org:1337/announce,udp://tracker.piratepublic.com:1337/announce,udp://tracker.publicbt.com:80/announce,udp://tracker.publictracker.xyz:6969/announce,udp://tracker.shkinev.me:6969/announce,udp://tracker.skynetcloud.site:6969/announce,udp://tracker.skyts.net:6969/announce,udp://tracker.swateam.org.uk:2710/announce,udp://tracker.teambelgium.net:6969/announce,udp://tracker.tiny-vps.com:6969/announce,udp://tracker.torrent.eu.org:451/announce,udp://tracker.tvunderground.org.ru:3218/announce,udp://tracker.uw0.xyz:6969/announce,udp://tracker.v6speed.org:6969/announce,udp://tracker.vulnix.sh:6969/announce,udp://tracker.yoshi210.com:6969/announce,udp://tracker.zemoj.com:6969/announce,udp://tracker.zerobytes.xyz:1337/announce,udp://tracker.zooki.xyz:6969/announce,udp://tracker.zum.bi:6969/announce,udp://tracker0.ufibox.com:6969/announce,udp://tracker1.itzmx.com:8080/announce,udp://tracker2.christianbro.pw:6969/announce,udp://tracker2.dler.org:80/announce,udp://tracker2.indowebster.com:6969/announce,udp://tracker2.itzmx.com:6961/announce,udp://tracker3.itzmx.com:6961/announce,udp://tracker4.itzmx.com:2710/announce,udp://tracker6.dler.org:2710/announce,udp://u.wwwww.wtf:1/announce,udp://ultra.zt.ua:6969/announce,udp://valakas.rollo.dnsabr.com:2710/announce,udp://vibe.community:6969/announce,udp://www.midea123.z-media.com.cn:6969/announce,udp://z.mercax.com:53/announce,udp://zephir.monocul.us:6969/announce,udp://zer0day.ch:1337/announce,udp://zer0day.to:1337/announce")
    aria2_daemon_start_cmd.append(f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}")
    #
    LOGGER.info(aria2_daemon_start_cmd)
    #
    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    LOGGER.info(stdout)
    LOGGER.info(stderr)
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=ARIA_TWO_STARTED_PORT,
            secret=""
        )
    )
    return aria2


def add_magnet(aria_instance, magnetic_link, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    try:
        download = aria_instance.add_magnet(
            magnetic_link,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


def add_torrent(aria_instance, torrent_file_path):
    if torrent_file_path is None:
        return False, "**FAILED** \n" + str(e) + " \nsomething wrongings when trying to add <u>TORRENT</u> file"
    if os.path.exists(torrent_file_path):
        # Add Torrent Into Queue
        try:
            download = aria_instance.add_torrent(
                torrent_file_path,
                uris=None,
                options=None,
                position=None
            )
        except Exception as e:
            return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
        else:
            return True, "" + download.gid + ""
    else:
        return False, "**FAILED** \n" + str(e) + " \nPlease try other sources to get workable link"


def add_url(aria_instance, text_url, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    uris = [text_url]
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(
            uris,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_unzip,
    is_unrar,
    is_untar,
    user_message
):
    if incoming_link.lower().startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    elif incoming_link.lower().endswith(".torrent"):
        sagtus, err_message = add_torrent(aria_instance, incoming_link)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    # https://stackoverflow.com/a/58213653/4723940
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p,
        None
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        #
        await asyncio.sleep(1)
        if err_message is not None:
            await check_progress_for_dl(
                aria_instance,
                err_message,
                sent_message_to_update_tg_p,
                None
            )
        else:
            return False, "can't get metadata \n\n#stopped"
    await asyncio.sleep(1)
    file = aria_instance.get_download(err_message)
    to_upload_file = file.name
    #
    if is_zip:
        # first check if current free space allows this
        # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
        # archive the contents
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    if to_upload_file:
        if CUSTOM_FILE_NAME:
            os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        else:
            to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    else:
        to_upload_file = to_upload_file
    #
    response = {}
    LOGGER.info(response)
    user_id = user_message.from_user.id
    print(user_id)
    final_response = await upload_to_tg(
        sent_message_to_update_tg_p,
        to_upload_file,
        user_id,
        response
    )
    LOGGER.info(final_response)
    try:
        message_to_send = ""
        for key_f_res_se in final_response:
            local_file_name = key_f_res_se
            message_id = final_response[key_f_res_se]
            channel_id = str(sent_message_to_update_tg_p.chat.id)[4:]
            private_link = f"https://t.me/c/{channel_id}/{message_id}"
            message_to_send += "👉 <a href='"
            message_to_send += private_link
            message_to_send += "'>"
            message_to_send += local_file_name
            message_to_send += "</a>"
            message_to_send += "\n"
        if message_to_send != "":
            mention_req_user = f"<a href='tg://user?id={user_id}'>Your Requested Files</a>\n\n"
            message_to_send = mention_req_user + message_to_send
            message_to_send = message_to_send + "\n\n" + "#uploads"
        else:
            message_to_send = "<i>FAILED</i> to upload files. 😞😞"
        await user_message.reply_text(
            text=message_to_send,
            quote=True,
            disable_web_page_preview=True
        )
    except:
        pass
    return True, None
#

async def call_apropriate_function_g(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_unzip,
    is_unrar,
    is_untar,
    user_message
):
    if incoming_link.lower().startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    elif incoming_link.lower().endswith(".torrent"):
        sagtus, err_message = add_torrent(aria_instance, incoming_link)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    # https://stackoverflow.com/a/58213653/4723940
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p,
        None
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        #
        await asyncio.sleep(1)
        if err_message is not None:
            await check_progress_for_dl(
                aria_instance,
                err_message,
                sent_message_to_update_tg_p,
                None
            )
        else:
            return False, "can't get metadata \n\n#stopped"
    await asyncio.sleep(1)
    file = aria_instance.get_download(err_message)
    to_upload_file = file.name
    #
    if is_zip:
        # first check if current free space allows this
        # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
        # archive the contents
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    if to_upload_file:
        if CUSTOM_FILE_NAME:
            os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        else:
            to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    else:
        to_upload_file = to_upload_file
    #
    response = {}
    LOGGER.info(response)
    user_id = user_message.from_user.id
    print(user_id)
    final_response = await upload_to_gdrive(
        to_upload_file,
        sent_message_to_update_tg_p,
        user_message,
        user_id
    )
#
async def call_apropriate_function_t(
    to_upload_file_g,
    sent_message_to_update_tg_p,
    is_unzip,
    is_unrar,
    is_untar
):
    #
    to_upload_file = to_upload_file_g
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file_g)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file_g)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file_g)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    response = {}
    LOGGER.info(response)
    user_id = sent_message_to_update_tg_p.reply_to_message.from_user.id
    final_response = await upload_to_gdrive(
        to_upload_file,
        sent_message_to_update_tg_p
    )
    LOGGER.info(final_response)
    #if to_upload_file:
        #if CUSTOM_FILE_NAME:
            #os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            #to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        #else:
            #to_upload_file = to_upload_file

    #if cstom_file_name:
        #os.rename(to_upload_file, cstom_file_name)
        #to_upload_file = cstom_file_name
    #else:
        #to_upload_file = to_upload_file
    '''
    
    LOGGER.info(final_response)
    message_to_send = ""
    for key_f_res_se in final_response:
        local_file_name = key_f_res_se
        message_id = final_response[key_f_res_se]
        channel_id = str(AUTH_CHANNEL)[4:]
        private_link = f"https://t.me/c/{channel_id}/{message_id}"
        message_to_send += "👉 <a href='"
        message_to_send += private_link
        message_to_send += "'>"
        message_to_send += local_file_name
        message_to_send += "</a>"
        message_to_send += "\n"
    if message_to_send != "":
        mention_req_user = f"<a href='tg://user?id={user_id}'>Your Requested Files</a>\n\n"
        message_to_send = mention_req_user + message_to_send
        message_to_send = message_to_send + "\n\n" + "#uploads"
    else:
        message_to_send = "<i>FAILED</i> to upload files. 😞😞"
    await sent_message_to_update_tg_p.reply_to_message.reply_text(
        text=message_to_send,
        quote=True,
        disable_web_page_preview=True
    )
    return True, None
    '''


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164
async def check_progress_for_dl(aria2, gid, event, previous_message):
    try:
        file = aria2.get_download(gid)
        complete = file.is_complete
        is_file = file.seeder
        if not complete:
            if not file.error_message:
                msg = ""
                # sometimes, this weird https://t.me/c/1220993104/392975
                # error creeps up
                # TODO: temporary workaround
                downloading_dir_name = "N/A"
                try:
                    # another derp -_-
                    # https://t.me/c/1220993104/423318
                    downloading_dir_name = str(file.name)
                except:
                    pass
                #
                msg = f"\nDownloading File: `{downloading_dir_name}`"
                msg += f"\nSpeed: {file.download_speed_string()} 🔽 / {file.upload_speed_string()} 🔼"
                msg += f"\nProgress: {file.progress_string()}"
                msg += f"\nTotal Size: {file.total_length_string()}"

                if is_file is None :
                   msg += f"\n<b>Connections:</b> {file.connections}"
                else :
                   msg += f"\n<b>Info:</b>[ P : {file.connections} || S : {file.num_seeders} ]"

                # msg += f"\nStatus: {file.status}"
                msg += f"\nETA: {file.eta_string()}"
                msg += f"\nGID: <code>{gid}</code>"
                inline_keyboard = []
                ikeyboard = []
                ikeyboard.append(InlineKeyboardButton("Cancel 🚫", callback_data=(f"cancel {gid}").encode("UTF-8")))
                inline_keyboard.append(ikeyboard)
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                #msg += reply_markup
                LOGGER.info(msg)
                if msg != previous_message:
                    await event.edit(msg, reply_markup=reply_markup)
                    previous_message = msg
            else:
                msg = file.error_message
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                await event.edit(f"`{msg}`")
                return False
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await check_progress_for_dl(aria2, gid, event, previous_message)
        else:
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await event.edit(f"File Downloaded Successfully: `{file.name}`")
            return True
    except Exception as e:
        LOGGER.info(str(e))
        if " not found" in str(e) or "'file'" in str(e):
            await event.edit("Download Canceled")
            return False
        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await event.edit("Download Auto Canceled\nYour Torrent/Link is Dead.")
            return False
        else:
            LOGGER.info(str(e))
            await event.edit("<u>error</u> :\n`{}` \n\n#error".format(str(e)))
            return
# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164


async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)
    LOGGER.info(file)
    if not file.followed_by_ids:
        # https://t.me/c/1213160642/496
        return None
    new_gid = file.followed_by_ids[0]
    LOGGER.info("Changing GID " + gid + " to " + new_gid)
    return new_gid
