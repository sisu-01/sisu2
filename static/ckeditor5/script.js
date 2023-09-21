ClassicEditor
	.create( document.querySelector("#editor"), {
		simpleUpload: {
			uploadUrl: upload_url,

            // Enable the XMLHttpRequest.withCredentials property.
            withCredentials: true,

            // Headers sent along with the XMLHttpRequest to the upload server.
            headers: {
                "X-CSRFToken": csrf_token,
                Authorization: "Bearer <JSON Web Token>"
            }
		}
	} )
	.then( editor => {
		window.editor = editor;
	} )
	.catch( handleSampleError );

function handleSampleError( error ) {
	const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

	const message = [
		'Oops, something went wrong!',
		`Please, report the following error on ${ issueUrl } with the build id "edsteai8845-ktylh53u5b3o" and the error stack trace:`
	].join( '\n' );

	console.error( message );
	console.error( error );
}
