"use strict";

const API_URL = document.location.origin;


async function make_request(method, url, data) {
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log(result);
    return result
}

async function make_post_request(url, data) {
    return await make_request("POST", url, data)
}

async function make_put_request(url, data) {
    return await make_request("PUT", url, data)
}

async function upload_avatar(url, file) {

    const formData = new FormData();
    formData.append('avatar', file);

    const response = await fetch(url, {
        method: "POST",
        body: formData
    });
    const result = await response.json();
    console.log(result);
    return result

}


async function deleteListing(listing_id) {
    const result = await make_request("DELETE", API_URL + "/cda/delete-listing/" + listing_id, null);
    console.log(result);
    location.reload();
}

async function upload_listing_images(url, files) {
    const formData = new FormData();
    for (const file of files) {
        formData.append('images', file);
    }
    const response = await fetch(url, {
        method: "POST",
        body: formData
    });
    const result = await response.json();
    console.log(result);
    return result
}


function contact_us_data(listing_id) {
    return {
        email: null,
        message: null,
        listing_id: listing_id,
        loading: false,
        messageSent: null,
        sendMessageToAdminUrl: API_URL + "/cda/admin/contact",
        sendMessageToAdmin: async function () {
            this.loading = true;

            const data = {
                message: this.message + "\nlisting_id=" + listing_id,
                email: this.email,
            };

            const result = await make_post_request(this.sendMessageToAdminUrl, data);

            if (result.status == 'success') {
                this.message = null;
                this.messageSent = true;
                setTimeout(() => this.messageSent = null, 3000);
            } else {
                this.messageSent = false;
                setTimeout(() => this.messageSent = null, 3000);
            }

            this.loading = false;
        }
    }
}


function send_message_data(listing_id, sendMsgToUserId, current_user_is_owner) {
    return {
        listing_id: listing_id,
        sendMsgToUserId: sendMsgToUserId,
        current_user_is_owner: current_user_is_owner,
        message: null,
        loading: false,
        messageSent: null,
        bigImg: false,
        showMsgModal: false,
        disableSendMsg: true,
        showDropDown: false,
        sentMessages: [],
        sendMessageUrl: API_URL + "/cda/send-message",
        markReadMessagesUrl: API_URL + "/cda/mark-read-messages",
        markAsReadMessages: async function (allMessages) {
            await make_post_request(this.markReadMessagesUrl, allMessages);
        },
        sendMessage: async function () {
            this.loading = true;

            const data = {
                message: this.message,
                listing_id: this.listing_id,
                to_user_id: this.sendMsgToUserId,
            };

            const result = await make_post_request(this.sendMessageUrl, data);

            this.loading = false;

            if (result.status == 'success') {
                this.sentMessages.push(this.message);
                this.message = null;
                this.showMsgModal = false;
                this.disableSendMsg = false;
                this.messageSent = true;
                setTimeout(() => this.messageSent = null, 3000);
            } else {
                this.messageSent = false;
            }
        }
    }
}

function create_listing_data() {
    return {
        titlu: null,
        oras: null,
        zona: null,
        pret: null,
        descriere: null,
        files: null,
        loading: false,
        showUpgradeInfo: false,
        redirectUrl: API_URL + "/cda/contul-meu",
        createListingUrl: API_URL + "/cda/create-listing",
        uploadListingImagesUrl: API_URL + "/cda/upload-images?listing_id=",
        createListing: async function () {
            this.loading = true;

            const data = {
                titlu: this.titlu,
                oras: this.oras,
                zona: this.zona,
                pret: this.pret,
                descriere: this.descriere,
            };

            const result = await make_post_request(this.createListingUrl, data);
            const result_images = await upload_listing_images(this.uploadListingImagesUrl + result.extra, this.files.slice(0, 3));

            this.loading = false;

            if (result.status == 'success' && result_images.status == 'success') {
                location.replace(this.redirectUrl);
            }

            if (result.content == "Doar un anunt postat este gratis.") {
                this.showUpgradeInfo = true;
            }

        }
    }
}

function delete_listing_data(listing_id) {
    return {
        listing_id: listing_id,
        redirectUrl: API_URL + "/cda/contul-meu",
        deleteUrl: API_URL + "/cda/delete-listings",
        deleteListing: async function () {
            this.loading = true;
            let data = [this.listing_id];
            console.log(data);
            const result = await make_request("DELETE", this.deleteUrl, data);
            this.loading = false;
            if (result.status == 'success') {
                location.replace(this.redirectUrl);
            }
        }
    }
}

function update_account_data() {
    return {
        nume: null,
        descriere: null,
        files: null,
        loading: false,
        updateFailed: false,
        updateAvatarUrl: API_URL + '/cda/upload-avatar',
        updateUrl: API_URL + '/cda/update-user',
        redirectUrl: API_URL + '/cda/contul-meu',
        update: async function () {

            this.loading = true;

            const data = {
                nume: this.nume,
                descriere: this.descriere
            };

            const result = await make_put_request(this.updateUrl, data);
            const result_avatar = await upload_avatar(this.updateAvatarUrl, this.files[0]);

            this.loading = false;

            if (result.status == 'success' && result_avatar.status == 'success') {
                location.replace(this.redirectUrl);
            } else {
                this.updateFailed = true;
            }
        }
    }
}


function login_data() {
    return {
        email: null,
        parola: null,
        loading: false,
        invalidcreds: false,
        loginUrl: API_URL + '/cda/login-user',
        redirectUrl: API_URL + '/cda/contul-meu',
        login: async function () {

            this.loading = true;

            const data = {
                email: this.email,
                parola: this.parola
            };

            const result = await make_post_request(this.loginUrl, data);

            this.loading = false;

            if (result.status == 'success') {
                location.replace(this.redirectUrl);
            } else {
                this.invalidcreds = true;
            }
        }
    }
}

function register_data() {
    return {
        email: null,
        parola: null,
        loading: false,
        confirmaparola: null,
        conditiiacceptate: false,
        registeredemail: false,
        invalidemailorpass: false,
        invalidpass: false,
        invalidconditii: false,
        redirectUrl: API_URL + '/cda/autentificare',
        registerUrl: API_URL + '/cda/create-user',
        register: async function () {

            this.loading = true;

            this.invalidconditii = !this.conditiiacceptate;
            this.invalidpass = this.parola != this.confirmaparola;

            if (this.invalidconditii || this.invalidpass) {
                this.loading = false;
                return
            }

            const data = {
                email: this.email,
                parola: this.parola
            };
            const result = await make_post_request(this.registerUrl, data);
            this.loading = false;

            this.registeredemail = result.content == 'Emailul este deja inregistrat.';
            this.invalidemailorpass = result.content == 'Emailul sau parola nu corespund cerintelor';
            if (result.status == 'success') {
                location.replace(this.redirectUrl);
            }
        }
    }
}
